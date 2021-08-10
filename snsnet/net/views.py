from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Health_Institution, Health_Professional, Post
from django.db import IntegrityError
from django_email_verification import send_email
from django.utils import timezone
from django.db.models import Value as V
from django.db.models.functions import Concat
import datetime


def login_redirect(request):
    """
    redirects to the login page
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        return HttpResponseRedirect(reverse('net:feed'))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def login_account(request):
    """
    if the form hasn't been filled: the login template is returned
    if the form has been filled: the login operation is performed and the feed template is returned
    :param request: session request
    """
    if request.method == 'POST':

        inputUsername = request.POST.get('inputUsername')
        inputPassword = request.POST.get('inputPassword')
        user = authenticate(request, username=inputUsername,
                            password=inputPassword)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('net:feed'))

        else:
            return render(request, 'net/login.html', {'error_message': "username ou password inválidos"})

    else:
        return render(request, 'net/login.html')


def health_professional_signup(request):
    """
    if the form hasn't been filled: the signup_health_professional template is returned
    if the form has been filled: the health professional account is created and an email verification is sent
    :param request: session request
    """
    if request.method == 'POST':

        first_name = request.POST.get('inputFirstName')
        last_name = request.POST.get('inputLastName')
        user_name = request.POST.get('inputUsername')
        email = request.POST.get('inputEmail')
        phone = request.POST.get('inputPhone')
        gender = request.POST.get('gender')
        district = request.POST.get('district')
        prof_type = request.POST.get('type')
        work = request.POST.get('work')
        password = request.POST.get('inputPassword')
        conf = request.POST.get('inputPasswordConfirmation')

        if '.' in user_name:
            error_message = 'o username contem um caracter inválido'
            institutions = Health_Institution.objects.all()
            return render(request, 'net/signup_health_professional.html', {'error_message': error_message,
                                                                           'institutions': institutions})

        if password != conf:
            error_message = 'as palavras-passe não coincidem'
            institutions = Health_Institution.objects.all()
            return render(request, 'net/signup_health_professional.html', {'error_message': error_message,
                                                                           'institutions': institutions})

        if gender == 'género' or district == 'distrito' or prof_type == 'tipo de profissional' \
                or work == 'onde trabalha':
            error_message = 'preenche corretamente os campos'
            institutions = Health_Institution.objects.all()
            return render(request, 'net/signup_health_professional.html', {'error_message': error_message,
                                                                           'institutions': institutions})

        try:
            user = User.objects.create_user(username=user_name, email=email, password=password,
                                            first_name=first_name, last_name=last_name, is_active=False)

        except IntegrityError:
            error_message = 'Este utilizador já está registado'
            institutions = Health_Institution.objects.all()
            return render(request, 'net/signup_health_professional.html', {'error_message': error_message,
                                                                           'institutions': institutions})

        if work == 'null':
            acc = Health_Professional()
            acc.user = user
            acc.phone = phone
            acc.gender = gender
            acc.district = district
            acc.type = prof_type
            acc.save()

        else:
            work = get_object_or_404(Health_Institution, pk=work)
            acc = Health_Professional()
            acc.user = user
            acc.phone = phone
            acc.gender = gender
            acc.district = district
            acc.type = prof_type
            acc.work = work
            acc.save()

        send_email(user)
        return render(request, 'net/email_sent.html', {'account': acc})

    else:
        institutions = Health_Institution.objects.all()
        return render(request, 'net/signup_health_professional.html', {'institutions': institutions})


def health_institution_signup(request):
    """
    if the form hasn't been filled: the signup_health_institution template is returned
    if the form has been filled: the health institution account is created and an email verification is sent
    :param request: session request
    """
    if request.method == 'POST':
        name = request.POST.get("inputName")
        user_name = request.POST.get('inputUsername')
        email = request.POST.get('inputEmail')
        phone = request.POST.get('inputPhone')
        district = request.POST.get('district')
        inst_type = request.POST.get('type')
        address = request.POST.get('inputAddress')
        password = request.POST.get('inputPassword')
        conf = request.POST.get('inputPasswordConfirmation')

        if password != conf:
            error_message = 'as palavras-passe não coincidem'
            return render(request, 'net/signup_health_institution.html', {'error_message': error_message})

        if inst_type == 'tipo de instituição' or district == 'distrito':
            error_message = 'preenche corretamente os campos'
            return render(request, 'net/signup_health_institution.html', {'error_message': error_message})

        try:
            user = User.objects.create_user(username=user_name, email=email, password=password,
                                            first_name=name, is_active=False)

        except IntegrityError:
            error_message = 'Esta instituição já está registada'
            return render(request, 'net/signup_health_institution.html', {'error_message': error_message})

        acc = Health_Institution()
        acc.user = user
        acc.district = district
        acc.address = address
        acc.phone = phone
        acc.type = inst_type
        acc.save()

        send_email(user)
        return render(request, 'net/email_sent.html')

    else:
        return render(request, 'net/signup_health_institution.html')


def resend_email(request):
    """
    resends the verification email if user is inactive
    :param request: session request
    """
    if request.method == 'POST':
        email = request.POST.get('inputEmail')

        try:
            user = User.objects.get(email=email)

        except ObjectDoesNotExist:
            return render(request, 'django_email_verification/confirmation.html', {
                'error_message': 'o email indicado nao está associado a nenhuma conta'
            })

        if user is not None:

            if not user.is_active:
                send_email(user)
                return render(request, 'net/email_sent.html')

            else:
                return render(request, 'django_email_verification/confirmation.html', {
                    'error_message': 'o email indicado já foi verificado'
                })
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def feed(request):
    """
    opens the feed page if the user is logged in
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)

        institution = False
        professional = False

        if isinstance(acc, Health_Professional):
            posts = get_posts_of_following(acc)
            professional = True
        else:
            posts = get_posts_of_institution_workers(acc)
            institution = can_post(acc)

        if request.method == 'POST':

            post = Post()
            post.user = acc.user
            post.likes = 0
            post.time = timezone.now()

            if isinstance(acc, Health_Professional):

                title = request.POST.get('title')

                if not title:
                    return render(request, 'net/feed.html', {'no_title': 'o post tem que ter um título',
                                                             'account': acc, 'posts': posts,
                                                             'institution': institution, 'professional': professional})
                post.title = title

                content = request.POST.get('content')
                image = request.FILES.get('image')

                if image is not None:
                    if not is_valid_image(str(image)):
                        return render(request, 'net/feed.html', {'invalid_image': 'formato de imagem inválido',
                                                                 'account': acc, 'posts': posts,
                                                                 'institution': institution,
                                                                 'professional': professional})
                    else:
                        post.image = image

                if content is not None:
                    post.content = content

            else:

                number = request.POST.get('cases')

                if not number:
                    return render(request, 'net/feed.html', {'no_title': 'número inválido',
                                                             'account': acc, 'posts': posts,
                                                             'institution': institution, 'professional': professional})

                title = 'contagem de dia ' + str(timezone.now().day) + ' do ' + str(
                    timezone.now().month) + ' de ' + str(timezone.now().year)
                content = 'Hoje, no ' + user.get_full_name() + ', foram registados ' + \
                    str(number) + ' casos.'

                post.title = title
                post.content = content

            post.save()

        return render(request, 'net/feed.html', {'account': acc, 'posts': posts,
                                                 'institution': institution, 'professional': professional})
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def like(request):
    """
    performs a like in a certain post (by ajax)
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:

        if request.is_ajax():

            acc = get_account(user)
            post_id = request.GET.get('post_id')
            post = Post.objects.get(pk=int(post_id))

            liked = False

            if isinstance(acc, Health_Institution):
                if acc in post.inst_likers.all():
                    post.inst_likers.remove(acc)
                    post.likes -= 1
                    post.save()
                    liked = False
                else:
                    post.inst_likers.add(acc)
                    post.likes += 1
                    post.save()
                    liked = True

            elif isinstance(acc, Health_Professional):
                if acc in post.prof_likers.all():
                    post.prof_likers.remove(acc)
                    post.likes -= 1
                    post.save()
                    liked = False
                else:
                    post.prof_likers.add(acc)
                    post.likes += 1
                    post.save()
                    liked = True

            return JsonResponse({'likes': post.likes, 'liked': str(liked)}, status=200)
        else:
            return HttpResponseRedirect(reverse('net:feed'))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def search(request):
    """
    performs the search of the database for a user through a string (by ajax)
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:

        if request.is_ajax():

            src = request.GET.get('search')
            users = User.objects.annotate(full_name=Concat('first_name', V(
                ' '), 'last_name')).filter(full_name__icontains=src)
            res = ''
            for user in users:
                s = "<a href='/account/" + user.username + \
                    "' style='text-decoration: none;' class='text-success'>" + user.full_name + "</a><br>"
                res += s

            return JsonResponse({'res': res}, status=200)
        else:
            return HttpResponseRedirect(reverse('net:feed'))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def delete_post(request, post_id):
    """
    delete a post
    :param request: session request
    :param post_id: the id of the post being deleted
    """
    user = request.user
    if user.is_authenticated:

        post = Post.objects.get(pk=post_id)
        post.delete()
        return HttpResponseRedirect(reverse('net:account', args=[user.username]))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def account(request, username):
    """
    shows the profile page of a selected account if the user is loggen in
    :param request: session request
    :param username: username of the account being shown
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)
        try:
            visited = get_account(User.objects.get(username=username))
            posts = get_my_posts(visited, acc)
            work = False

            if isinstance(visited, Health_Professional):
                if visited.work:
                    work = True

            if isinstance(acc, Health_Professional):

                if not is_following(acc, visited):
                    return render(request, 'net/account_general.html', {'account': acc, 'visited': visited,
                                                                        'follow': True, 'work': work, 'posts': posts})
                else:
                    return render(request, 'net/account_general.html', {'account': acc, 'visited': visited,
                                                                        'unfollow': True, 'work': work, 'posts': posts})
            else:
                return render(request, 'net/account_general.html', {'account': acc, 'visited': visited, 'posts': posts,
                                                                    'work': work})
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('net:not_found'))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def logout_account(request):
    """
    logout the user
    :param request: session request
    """
    logout(request)
    return HttpResponseRedirect(reverse('net:login_account'))


def upload_image(request):
    """
    uploads an image to the account photo field
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)
        if request.method == 'POST':
            image = request.FILES.get('image')
            if is_valid_image(str(image)):
                acc.photo = image
                acc.save()
        return HttpResponseRedirect(reverse('net:account', args=[user.username]))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def update_personal_info(request):
    """
    updates some of the information of an User
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)
        if request.method == 'POST':
            name = update_field(user.get_full_name(),
                                request.POST.get('inputName'))

            head, *tail = name.split(" ")
            if not tail:
                return render(request, 'net/update_personal_info.html', {'account': acc,
                                                                         'error_message': 'nome preenchido '
                                                                                          'incorretamente'})
            else:
                first_name = head
                last_name = ""
                for name in tail:
                    last_name = last_name + name + " "
                user.first_name = first_name
                user.last_name = last_name

            username = update_field(user.username,
                                    request.POST.get('inputUsername'))
            if '.' in username:
                error_message = 'o username contem um caracter inválido'
                return render(request, 'net/update_personal_info.html', {'account': acc,
                                                                         'error_message': error_message})
            else:
                user.username = username

            phone = update_field(acc.phone,
                                 request.POST.get('inputPhone'))
            acc.phone = phone

            try:
                user.save()
                acc.save()
                return HttpResponseRedirect(reverse('net:account', args=[user.username]))
            except IntegrityError:
                return render(request, 'net/update_personal_info.html', {'account': acc,
                                                                         'error_message': 'nome de utilizador já '
                                                                                          'registado'})

        else:
            return render(request, 'net/update_personal_info.html', {'account': acc})
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def update_password(request):
    """
    updates the password of the currently logged user
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            password = request.POST.get('inputPassword')
            new_password = request.POST.get('inputNewPassword')
            new_password_conf = request.POST.get(
                'inputNewPasswordConfirmation')

            if password.strip() and new_password.strip() and new_password_conf.strip():

                if user.check_password(password):

                    if new_password != new_password_conf:
                        return render(request, 'net/update_password.html', {
                            'error_message': 'as novas passwords não coincidem'
                        })
                    else:
                        user.set_password(new_password)
                        user.save()
                        logout(request)
                        return render(request, 'net/data_updated.html')

                else:
                    return render(request, 'net/update_password.html', {'error_message': 'password atual incorreta'})
            else:
                return render(request, 'net/update_password.html', {
                    'error_message': 'preenche todos os campos'
                })
        else:
            return render(request, 'net/update_password.html')
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def follow(request, username):
    """
    performs the action of following an account with the given username
    :param request: session request
    :param username: the username of the account being followed
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)
        visited = get_account(User.objects.get(username=username))

        if isinstance(visited, Health_Professional):
            acc.following_prof.add(visited)
        elif isinstance(visited, Health_Institution):
            acc.following_inst.add(visited)

        acc.save()
        return HttpResponseRedirect(reverse('net:account', args=[username]))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def unfollow(request, username):
    """
    performs the action of unfollowing an account with the given username
    :param request: session request
    :param username: the username of the account being unfollowed
    """
    user = request.user
    if user.is_authenticated:
        acc = get_account(user)
        visited = get_account(User.objects.get(username=username))
        if isinstance(visited, Health_Professional):
            acc.following_prof.remove(visited)
        elif isinstance(visited, Health_Institution):
            acc.following_inst.remove(visited)
        acc.save()
        return HttpResponseRedirect(reverse('net:account', args=[username]))
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def not_found(request):
    """
    open a 404 page
    :param request: session request
    """
    user = request.user
    if user.is_authenticated:
        return render(request, 'net/404.html')
    else:
        return HttpResponseRedirect(reverse('net:login_account'))


def get_account(user):
    """
    gets the model Class object in which the User is registered.
    doesn't throws an exception: that verification is done previously
    :param user: django.contrib.auth.models.User object
    :return: model Class object
    """
    try:
        acc = Health_Institution.objects.get(user=user)
    except ObjectDoesNotExist:
        acc = Health_Professional.objects.get(user=user)
    return acc


def is_valid_image(filename):
    """
    indicates if the given image is png, jpg or jpeg (valid formats)
    :param filename: the name of the image file
    :return: True if the file format is one of the three mentioned (False if not)
    """
    split_array = filename.split('.')
    valid_images = ['png', 'jpg', 'jpeg']
    image_format = split_array[len(split_array) - 1]
    if image_format in valid_images:
        return True
    else:
        return False


def is_following(follower, followed):
    """
    checks if the follower account is following the followed accounts
    :param follower: the account that follows
    :param followed: the account that is following
    :return True if there is a following relationship
    """
    if isinstance(followed, Health_Professional):
        for following in follower.following_prof.all():
            if following.id is followed.id:
                return True
    elif isinstance(followed, Health_Institution):
        for following in follower.following_inst.all():
            if following.id is followed.id:
                return True
    return False


def get_my_posts(acc, visiting):
    """
    get the posts of one account
    :param acc: the owner of the posts
    :param visiting: the account trying to get access to the posts
    :return: a list of tuples (post, owner of the post, if the visiting account has liked the post)
    """
    my_posts = []
    for post in Post.objects.order_by('-time', '-likes'):
        if post.user.id is acc.user.id:
            liked = visiting in post.inst_likers.all() or visiting in post.prof_likers.all()
            my_posts.append((post, acc, liked))
    return my_posts


def get_posts_of_following(acc):
    """
    gets the posts of all the account that are being followed
    :param acc: the account trying to get access to the posts
    :return: a list of tuples (post, owner of the post, if the visiting account has liked the post)
    """
    posts = []
    for post in Post.objects.order_by('-likes', '-time'):
        if post.is_recent():
            author = get_account(post.user)
            if author in acc.following_prof.all() or author in acc.following_inst.all():
                liked = acc in post.inst_likers.all() or acc in post.prof_likers.all()
                posts.append((post, author, liked))
    return posts


def get_posts_of_institution_workers(acc):
    """
    gets the posts of all the health professionals that work in that institution
    :param acc: the institution account
    :return: a list of tuples (post, owner of the post, if the visiting account has liked the post)
    """
    posts = []
    for post in Post.objects.order_by('-likes', '-time'):
        if post.is_recent():
            worker = get_account(post.user)
            if isinstance(worker, Health_Professional):
                if worker.work is not None and worker.work.id is acc.id:
                    liked = acc in post.inst_likers.all() or acc in post.prof_likers.all()
                    posts.append((post, worker, liked))
    return posts


def update_field(old, new):
    """
    check if the new field has been filled
    :param old: old field
    :param new: new field
    :return: the field that be used to update the account
    """
    if new.strip():
        return new
    else:
        return old


def can_post(acc):
    """
    check if there is any post by the account in the last 24 hours
    :param acc: the account being verified
    :return: true if there's no post in the last 24 hours
    """
    my_posts = get_my_posts(acc, acc)
    if len(my_posts) > 0:
        last_post_time = get_my_posts(acc, acc)[0][0].time
        return not last_post_time >= timezone.now() - datetime.timedelta(days=1)
    else:
        return True
