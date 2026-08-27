import os
import json
from http.server import BaseHTTPRequestHandler
from openai import OpenAI


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            # 요청 데이터 읽기
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body)

            destination = data.get("destination", "").strip()
            duration = data.get("duration", "").strip()
            style = data.get("style", "").strip()

            # 빈 입력 확인
            if not destination or not duration or not style:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {
                    "error": "여행지, 여행 기간, 여행 스타일을 모두 입력해주세요."
                }

                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
                return

            # API 키 가져오기
            api_key = os.environ.get("OPENAI_API_KEY")

            if not api_key:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                response = {
                    "error": "AI API 키가 설정되지 않았습니다."
                }

                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
                return

            # OpenAI 클라이언트
            client = OpenAI(api_key=api_key)

            # AI에게 보낼 요청
            prompt = f"""
당신은 친절한 여행 플래너입니다.

다음 정보를 바탕으로 여행 일정을 추천해주세요.

여행지: {destination}
여행 기간: {duration}
여행 스타일: {style}

날짜별로 보기 쉽게 여행 일정을 작성해주세요.
각 날짜마다 추천 장소와 간단한 설명을 포함해주세요.
너무 빡빡하지 않고 현실적인 일정으로 작성해주세요.
한국어로 답변해주세요.
"""

            response = client.responses.create(
                model="gpt-5-mini",
                input=prompt
            )

            result = response.output_text

            # 결과 반환
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            output = {
                "result": result
            }

            self.wfile.write(
                json.dumps(output, ensure_ascii=False).encode("utf-8")
            )

        except Exception as e:

            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            output = {
                "error": "AI 추천을 만드는 중 문제가 발생했습니다."
            }

            self.wfile.write(
                json.dumps(output, ensure_ascii=False).encode("utf-8")
            )
