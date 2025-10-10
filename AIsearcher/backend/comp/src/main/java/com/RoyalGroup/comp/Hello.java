// package com.RoyalGroup.comp;

// @restController

// @RestController
// public class Hello {
//     @GetMapping("/")
//     public String sayHello() {
//         return "Hello, World!";
//     }
// }


package com.RoyalGroup.comp;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class Hello {

    @GetMapping("/hello")
    public String sayHello() {
        return "Hello from Spring Boot in Codespaces!";
    }
}
