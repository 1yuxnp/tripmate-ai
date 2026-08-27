import os
import json
from http.server import BaseHTTPRequestHandler
from google import genai


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            "TripMate AI API가 정상적으로 작동합니다.".encode("utf-8")
        )

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            destination = data.get("destination", "").strip()
            duration = data.get("duration", "").strip()
            style = data.get("style", "").strip()

            if not destination or not duration or not style:
                self.send_response(400)
                self.send_header(
                    "Content-Type",
                    "application/json; charset=utf-8"
                )
                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "error": "여행지, 여행 기간, 여행 스타일을 모두 입력해주세요."
                    }, ensure_ascii=False).encode("utf-8")
                )
                return

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self.send_response(500)
                self.send_header(
                    "Content-Type",
                    "application/json; charset=utf-8"
                )
                self.end_headers()

                self.wfile.write(
                    json.dumps({
                        "error": "Gemini API 키가 설정되지 않았습니다."
                    }, ensure_ascii=False).encode("utf-8")
                )
                return

            client = genai.Client(api_key=api_key)

            prompt = f"""
당신은 친절한 AI 여행 플래너입니다.

여행지: {destination}
여행 기간: {duration}
여행 스타일: {style}

위 정보를 바탕으로 현실적인 여행 일정을 추천해주세요.

날짜별로 구분하고,
추천 장소와 간단한 설명을 포함해주세요.
너무 빡빡하지 않은 일정으로 작성해주세요.
한국어로 답변해주세요.
"""

           response = client.models.generate_content(
           model="gemini-3.6-flash",
           contents=prompt
           )


            result = response.text

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "result": result
                }, ensure_ascii=False).encode("utf-8")
            )

        except Exception as e:
            print("ERROR:", e)

            self.send_response(500)
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "error": "AI 추천을 만드는 중 문제가 발생했습니다."
                }, ensure_ascii=False).encode("utf-8")
            )
