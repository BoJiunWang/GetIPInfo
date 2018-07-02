import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Properties;
import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

/**
 * Created by Ivan_Wang on 2018-05-23.
 */
public class Main {

  public static void sendMail(final String[] mailAddresses, final String ip) {

    Properties props = new Properties();
    props.put("mail.smtp.auth", "true");
    props.put("mail.smtp.starttls.enable", "true");
    props.put("mail.smtp.host", "smtp.gmail.com");
    props.put("mail.smtp.ssl.trust", "smtp.gmail.com");
    props.put("mail.smtp.port", "587");
    final String userName = "account";
    final String password = "password";

    Session session = Session.getInstance(props, new Authenticator() {
      protected PasswordAuthentication getPasswordAuthentication() {
        return new PasswordAuthentication(userName, password);
      }
    });

    try {
      StringBuilder sb = new StringBuilder();
      BufferedReader in = new BufferedReader(
          new InputStreamReader(new FileInputStream("ip.txt"), StandardCharsets.UTF_8));
      String strNum;
      while ((strNum = in.readLine()) != null) {
        sb.append(strNum);
      }
      if (!sb.toString().equals(ip)) {
        MimeMessage message = new MimeMessage(session);
        InternetAddress me = new InternetAddress(userName);
        me.setPersonal("Ivan Wang");
        message.setFrom(me);
        if (mailAddresses.length != 0) {
          for (String mailAddress : mailAddresses) {
            message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(mailAddress));
          }
        } else {
          message
              .setRecipients(Message.RecipientType.TO, InternetAddress.parse("defaultmail@gmail.com"));
        }
        message.setSubject("IP has been modified!", "UTF-8");
        message.setText("New IP is: " + ip, "UTF-8");
        Transport.send(message);

        BufferedWriter bufferedWriter = new BufferedWriter(
            new OutputStreamWriter(new FileOutputStream("ip.txt"), StandardCharsets.UTF_8));
        bufferedWriter.write(ip);
        bufferedWriter.flush();
        bufferedWriter.close();
      }
      in.close();
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  public static String getIpAddress() {
    String systemIpAddress;
    try {
      URL urlPath = new URL("https://bot.whatismyipaddress.com");
      BufferedReader sc =
          new BufferedReader(new InputStreamReader(urlPath.openStream(), StandardCharsets.UTF_8));
      systemIpAddress = sc.readLine();
      sc.close();
    } catch (Exception e) {
      systemIpAddress = "Cannot Execute Properly, Check %s is workable!";
      e.printStackTrace();
    }
    return systemIpAddress;
  }

  public static boolean createTxt() {
    String path = "./ip.txt";
    File f = new File(path);
    boolean isSuccess = false;
    try {
      isSuccess = f.createNewFile();
    } catch (Exception e) {
      e.printStackTrace();
    }
    return isSuccess;
  }

  public static void main(String[] args) {
    createTxt();
    sendMail(args, getIpAddress());
  }
}
