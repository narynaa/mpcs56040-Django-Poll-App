import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = "http://127.0.0.1:8000";
const POLL_ID = 1;
const CHOICE_ID = 2;

export const options = {
    stages: [
        { duration: "10s", target: 100 },
        { duration: "1m", target: 100 },
        { duration: "10s", target: 0 },
    ],
};

function getCsrf(html) {
    const match = html.match(/name="csrfmiddlewaretoken" value="([^"]+)"/);
    return match ? match[1] : "";
}

export default function () {
    const username = `k6user${(__VU % 200) + 1}`;

    let loginPage = http.get(`${BASE_URL}/accounts/login/`);
    let csrf = getCsrf(loginPage.body);

    let loginRes = http.post(`${BASE_URL}/accounts/login/`, {
        username: username,
        password: "password123",
        csrfmiddlewaretoken: csrf,
    });

    let list = http.get(`${BASE_URL}/polls/list/`);
    let detail = http.get(`${BASE_URL}/polls/${POLL_ID}/`);

    let votePage = http.get(`${BASE_URL}/polls/${POLL_ID}/`);
    let voteCsrf = getCsrf(votePage.body);

    let vote = http.post(`${BASE_URL}/polls/${POLL_ID}/vote/`, {
        choice: CHOICE_ID,
        csrfmiddlewaretoken: voteCsrf,
    });

    check(loginRes, { "login ok": r => r.status === 200 || r.status === 302 });
    check(list, { "list ok": r => r.status === 200 });
    check(detail, { "detail ok": r => r.status === 200 });
    check(vote, { "vote ok": r => r.status === 200 || r.status === 302 });

    sleep(1);
}