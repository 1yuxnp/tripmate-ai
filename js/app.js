const button = document.getElementById("recommend-button");

button.addEventListener("click", async function () {

    const destination =
        document.getElementById("destination").value.trim();

    const duration =
        document.getElementById("duration").value.trim();

    const style =
        document.getElementById("style").value.trim();

    const result =
        document.getElementById("result");


    // 1. 빈 입력 확인
    if (!destination || !duration || !style) {

        result.textContent =
            "⚠️ 여행지, 여행 기간, 여행 스타일을 모두 입력해주세요.";

        return;
    }


    // 2. 로딩 표시
    result.textContent =
        "🤖 AI가 여행 일정을 만드는 중입니다...";


    try {

        // 3. Python API 호출
        const response = await fetch("/api/recommend", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                destination: destination,
                duration: duration,
                style: style
            })
        });


        // 4. 서버 응답 받기
        const data = await response.json();


        // 5. API 오류 처리
        if (!response.ok) {

            result.textContent =
                "⚠️ " + (data.error || "AI 추천을 불러오지 못했습니다.");

            return;
        }


        // 6. AI 결과 화면에 표시
        result.textContent =
            data.result;


    } catch (error) {

        console.error(error);

        result.textContent =
            "⚠️ 서버와 연결할 수 없습니다. 잠시 후 다시 시도해주세요.";
    }

});
