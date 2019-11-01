#include <iostream>
#include <cpr/cpr.h>

int main() {
    auto r = cpr::Get(cpr::Url{"https://self-signed.badssl.com/"});
    std::cout << r.status_code;                  // 200
    std::cout << r.header["content-type"];       // application/json; charset=utf-8
    std::cout << r.text;                         // JSON text string
}