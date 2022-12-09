from django import forms
from pybo.models import Question, Answer


# 폼 : 페이지 요청시 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 클래스
# 필수 파라미터의 값이 누락되지 않았는지, 파라미터의 형식은 적절한지 등을 검증할 목적으로 사용
# 모델 폼은 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼
# 이너 클래스인 Meta 클래스가 반드시 필요
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question # 사용할 모델
        fields = ['content', 'imgfile'] # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
        labels = {
            'content': '내용',
            'imgfile': '이미지',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }