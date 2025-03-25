# users/cb_views.py

from django.contrib.auth import get_user_model, login
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView
from users.forms import SignupForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect

from utils.email import send_email

User = get_user_model()


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm

    def form_valid(self, form):
        user = form.save()
        # 인증 메일 발송
        signer = TimestampSigner()  # 특정 정보를 암호화해서 보냄
        # 1. 이메일에 서명
        signed_user_email = signer.sign(user.email)
        # 2. 서명된 이메일을 직렬화
        signer_dump = signing.dumps(signed_user_email)

        url = f"{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signer_dump}"
        subject = f"[Todo]{user.email}님의 이메일 인증 링크입니다."
        message = f"""
            아래의 링크를 클릭하여 이메일 인증을 완료해주세요.\n\n
            {url}
            """
        send_email(subject=subject, message=message, from_email=None, to_email=user.email)

        return render(
            request=self.request,
            template_name="registration/signup_done.html",
            context={
                'user': user,
            }
        )


def verify_email(request):
    code = request.GET.get('code', '')  # code가 없으면 공백으로 처리

    signer = TimestampSigner()
    try:
        # 3. 직렬화된 데이터를 역직렬화
        decoded_user_email = signing.loads(code)
        # 4. 타임스탬프 유효성 검사 포함하여 복호화
        user_email = signer.unsign(decoded_user_email, max_age=60 * 5)  # 5분 설정
    except (TypeError, SignatureExpired):  # 시간 지나서 오류발생하면 오류처리
        return render(request, 'registration/verify_failed.html')

    user = get_object_or_404(User, email=user_email)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html')


class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("cbv_todo_list")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user=user)
        return HttpResponseRedirect(self.get_success_url())