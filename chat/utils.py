import fitz
from django.conf import settings
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def get_completion(prompt, model="gpt-3.5-turbo"):
    """
    OpenAI API를 사용하여 prompt에 대한 completion 생성
    :param prompt: prompt
    :param model: 사용할 AI 모델
    :return: completion
    """
    try:
        chat_completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.5,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def generate_prompt(text_input, file_input, youtube_url):
    """
    prompt 생성
    :param text_input: 입력한 내용
    :param file_input: 업로드한 파일
    :param youtube_url: 유튜브 URL
    :return: prompt
    """
    if text_input:
        return f"다음 내용을 10줄 이내로 요약해주세요: {text_input}"
    elif file_input:
        file_content = extract_text_from_pdf(file_input)
        return f"다음 PDF 파일 내용을 10줄 이내로 요약해주세요: {file_content}"
    elif youtube_url:
        youtube_content = extract_text_from_youtube(youtube_url)
        return f"다음 유튜브 비디오 내용을 10줄 이내로 요약해주세요: {youtube_content}"
    else:
        return "요약할 내용이 없습니다."


def extract_text_from_pdf(pdf_file):
    """
    pdf 파일에서 텍스트 추출
    :param pdf_file: pdf 파일
    :return: pdf 파일의 텍스트
    """
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text


def extract_text_from_youtube(youtube_url):
    """
    youtube 비디오에서 자막 추출
    :param youtube_url: youtube url
    :return: youtube 비디오의 자막
    """
    video_id = youtube_url.split("v=")[-1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    transcript_text = " ".join([line["text"] for line in transcript])
    return transcript_text


def translate_to_korean(text, model="gpt-3.5-turbo"):
    try:
        translation_prompt = \
            f"Translate the following English text to Korean: {text}"
        translation_completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": translation_prompt}],
                max_tokens=150,
                temperature=0.5,
        )
        return translation_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred during translation: {e}"
