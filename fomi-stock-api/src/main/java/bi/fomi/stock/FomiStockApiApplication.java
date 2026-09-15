package bi.fomi.stock;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class FomiStockApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(FomiStockApiApplication.class, args);
    }
}
