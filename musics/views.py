from django.shortcuts import render, redirect

# Create your views here.
from musics.forms import LoginForm, NewSongForm, NewUserForm, QueryForm, Qform
from musics.models import Student, Song
from itertools import chain

def home(request):
    note = " Please insert your Username/Password or register if you are a new user"
    if request.method == 'POST':
        userpass = LoginForm(request.POST)
        if userpass.is_valid():
            _username = userpass.cleaned_data['username']
            _password = userpass.cleaned_data['password']
            try:
                instance = Student.objects.get(username=_username)
                if instance.password == _password:

                    return redirect(mainpage, s_id= instance.pk)

                else:
                    note = "Wrong Password! Try again."
                    newform = LoginForm()
                    return render(request, 'musics/home.html', {'userid': newform, 'note':note})
            except Student.DoesNotExist:
                instance = None
            newform = LoginForm()
            return render(request, 'musics/home.html', {'userid': newform, })
    else:
        form = LoginForm()
        return render(request, 'musics/home.html', {'userid': form, 'note':note})

def mainpage(request, s_id):
    newMusicform = NewSongForm()
    query = Qform()
    note = ""
    try:
        qresult=None
        student = Student.objects.get(pk=s_id)

        songs = student.song.all()

    except Student.DoesNotExist:
        raise home(request)
    if request.method == 'POST':

        query = Qform(request.POST)
        if query.is_valid():
            qresult= []
            criteria1 = query.cleaned_data["title"] if len(query.cleaned_data["title"] )!= 0 else " "

            criteria2 = query.cleaned_data["year"] if (query.cleaned_data["year"] != None) else 0

            criteria3 = query.cleaned_data["artist"] if len(query.cleaned_data["artist"] )!= 0 else " "
            Song.objects.filter(title__contains= criteria1, year = None).delete()
            Song.objects.filter(artist__contains=criteria3, year=None).delete()
            Song.objects.filter(title=None).delete()
            qresult1= Song.objects.filter(title__contains= criteria1) if criteria1 != " " else Song.objects.all()
            qresult2 = Song.objects.filter(year= criteria2) if (criteria2 != 0) else Song.objects.all()
            qresult3 = Song.objects.filter(artist__contains= criteria3) if criteria3 != " " else Song.objects.all()

            qresult = qresult1.intersection(qresult3, qresult2)

            if len(qresult)==0:
                note= "No result found"

    newMusicform = NewSongForm()
    return render(request, 'musics/mainpage.html', {'student': student, 'newSongform': newMusicform, 'query': query, 'qresult': qresult, 'note': note, 'songs': songs, })

def signup(request):
    note = ""
    if request.method == 'POST':
        registered = NewUserForm(request.POST, request.FILES)

        form = LoginForm()
        if registered.is_valid():

            if registered.valid_password():
                registered.save()
                note = " You are registered now!"
            else:
                note = "Your password should be match in both fields"
                registered = NewUserForm()
                print("not match")
                return render(request, 'musics/registration.html', {'registered': registered, 'note': note,})

        return render(request, 'musics/home.html', {'userid': form, 'note': note, })
    else:
        registered = NewUserForm()
        return render(request, 'musics/registration.html', {'registered': registered, })

def addmusic(request, s_id):
    newMusicform = NewSongForm()
    note = "Please insert the song specifications in the form"
    try:
        qresult=None
        student = Student.objects.get(pk=s_id)

        songs = Song.objects.all()

    except Student.DoesNotExist:
        raise home(request)
    if request.method == 'POST':
        newMusicform = NewSongForm(request.POST, request.FILES)

        if newMusicform.is_valid():
            obj = newMusicform.save(commit=False)
            obj.likedBy = Student.objects.get(pk=s_id)
            obj.save()
            note = " Your new song is registered successfully"
    newMusicform = NewSongForm()
    return render(request, 'musics/addmusic.html', {'student': student, 'newSongform': newMusicform, 'note': note, })

def subscribe(request, s_id, m_id):
    note=''
    student = Student.objects.get(pk=s_id)
    song = Song.objects.get(pk=m_id)
    if request.method == 'POST':
        song.likedBy=student
        student.song.add(song)
        note= "This music is added to your subscriptions"
    return render(request, 'musics/subscribe.html', {'student': student, 'song': song, 'note': note, })

