#include <iostream>
#include <cpr/cpr.h>
#include <algorithm>
#include <zconf.h>
#include <fstream>
#include "json.h"

using namespace nlohmann;

std::string TOKEN;

const std::string GET_UPDATES = "getUpdates";
const std::string SEND_MESSAGE = "sendMessage";

json sendRequest(const std::string &method, const cpr::Parameters &params) {
    auto url = "https://api.telegram.org/bot" + TOKEN + "/" + method;
    auto response = cpr::Get(cpr::Url{url}, params);
    if (response.status_code == 0) {
        throw std::runtime_error(response.error.message);
    }
    std::cout << response.text << "\n";
    return json::parse(response.text);
}

json getUpdates(int lastUpdate = 0) {
    cpr::Parameters params = {{"allowed_updates", "message"},
                              {"timeout",         "10"}};
    if (lastUpdate != 0) {
        params.AddParameter({"offset", std::to_string(lastUpdate)});
    }
    auto response = sendRequest(GET_UPDATES, params);
    return response["result"];
}

void sendMessage(const std::string &text, long long chat_id) {
    try {
        sendRequest(SEND_MESSAGE, {{"text",    text},
                                   {"chat_id", std::to_string(chat_id)}});
    } catch (std::exception &e) {
        std::cerr << "Couldn't write back to " << chat_id << " because: " << e.what();
    }
}

void processNewMessage(json &update) {
    auto message = update["message"];
    auto chat_id = message["chat"]["id"].get<long long>();
    std::string text = message["text"].get<std::string>();
    std::transform(text.begin(), text.end(), text.begin(),
                   [](unsigned char c) { return std::tolower(c); });

    if (message.find("entities") != message.end() && message["entities"][0]["type"] == "bot_command") {
        if (text == "/woof") {
            sendMessage("👎", chat_id);
        } else if (text == "/miu") {
            sendMessage("👍", chat_id);
        }
    } else if (text.find("миу") != std::string::npos) {
        sendMessage("миу!", chat_id);
    } else if (text.find("мяу") != std::string::npos) {
        sendMessage("не мяу, а миу!", chat_id);
    } else if (text.find("гав") != std::string::npos) {
        sendMessage("не гав, а /woof", chat_id);
    }
}


int main() {
    std::ifstream tokenFile("token.txt");
    std::string tempToken((std::istreambuf_iterator<char>(tokenFile)),
                          std::istreambuf_iterator<char>());
    TOKEN = json::parse(tempToken)["token"];
    std::cout << TOKEN;

    int lastUpdate = 0;
    while (true) {
        try {
            auto updates = getUpdates(lastUpdate);
            for (auto &update: updates) {
                lastUpdate = std::max(lastUpdate, update["update_id"].get<int>() + 1);
                processNewMessage(update);
            }
        } catch (std::exception &e) {
            std::cerr << "Unable to get updates: " << e.what() << "\n";
            sleep(1);
        }
    }
}