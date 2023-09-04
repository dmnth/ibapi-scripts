import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

public class sendGet {
    public static void main(String[] args) throws Exception {
	TrustManager[] trustAllCerts = new TrustManager[] {
            new X509TrustManager() {
                public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                    return new java.security.cert.X509Certificate[] {};
                }
                public void checkClientTrusted(
                    java.security.cert.X509Certificate[] certs, String authType) {}
                public void checkServerTrusted(
                    java.security.cert.X509Certificate[] certs, String authType) {}
            }
        };

        // Create an SSL context that uses the trust manager
        SSLContext sslContext = SSLContext.getInstance("SSL");
        sslContext.init(null, trustAllCerts, new java.security.SecureRandom());

        SSLParameters sslParams = new SSLParameters();
        sslParams.setEndpointIdentificationAlgorithm(null);
        HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());
        HttpsURLConnection.setDefaultHostnameVerifier((hostname, session) -> true);
        URL url = new URL("https://192.168.1.167:5000/v1/api/portfolio/accounts");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("GET");

        BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
        String inputLine;
        StringBuffer response = new StringBuffer();
        while ((inputLine = in.readLine()) != null) {
            response.append(inputLine);
        }
        in.close();

        // Print the response
        System.out.println(response.toString());
    }
}
