#include <WiFi.h>
#include <HTTPClient.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "";
const char* password = "";

const char* influxHost = "";
const char* influxToken = "2lGFfU5nOF74whOHM1KXRAo-QQ992L9CplVHA_HfXZVI2NsDzRg1y-LbvMSonWdCa9futTqEtht68Tt0kXPBpQ=="; // fake token
const char* influxOrg = "public";
const char* influxBucket = "public";

AsyncWebServer server(80);

String getStatus() {
  HTTPClient http;

  http.begin(String(influxHost) + "/api/v2/query?org=" + influxOrg);
  http.addHeader("Authorization", "Token " + String(influxToken));
  http.addHeader("Content-Type", "application/vnd.flux");
  http.addHeader("Accept", "application/csv");

  String fluxQuery = R"(
    from(bucket: "public")
      |> range(start: -1h)
      |> filter(fn: (r) => r["_measurement"] == "status")
  )";

  int httpResponseCode = http.POST(fluxQuery);
  String payload;

  if (httpResponseCode > 0) {
    payload = http.getString();
  } else {
    payload = String(httpResponseCode);
  }

  http.end();

  return payload;
}

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("Connected to WIFI!");

  server.on("/status", HTTP_GET, [](AsyncWebServerRequest* request) {
    request->send(200, "text/plain", getStatus());
  });

  server.begin();
}

void loop() {
  // nothing here
}
