package cs.ubbcluj.ro.license.controller;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.*;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import cs.ubbcluj.ro.license.payload.request.LoginRequest;
import cs.ubbcluj.ro.license.repository.RoleRepository;
import cs.ubbcluj.ro.license.repository.UserRepository;
import cs.ubbcluj.ro.license.security.WebSecurityConfig;
import cs.ubbcluj.ro.license.security.jwt.AuthEntryPointJwt;
import cs.ubbcluj.ro.license.security.jwt.JwtUtils;
import cs.ubbcluj.ro.license.security.services.UserDetailsServiceImpl;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.RequestBuilder;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestBuilders.formLogin;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(AuthController.class)
@ExtendWith(SpringExtension.class)
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private AuthenticationManager authenticationManager;

    @MockBean
    private UserRepository userRepository;

    @MockBean
    private RoleRepository roleRepository;

    @MockBean
    private PasswordEncoder encoder;

    @MockBean
    private JwtUtils jwtUtils;

    @MockBean
    private UserDetailsServiceImpl userDetailsService;

    @MockBean
    private AuthEntryPointJwt authEntryPointJwt;

    @Test
    void authenticateUserSuccess() throws Exception {
        MockHttpServletRequestBuilder post = post("/api/auth/signin").contentType("application/json")
                .content(objectMapper.writeValueAsString(createLoginRequest()));

        ResultActions resultActions = mockMvc.perform(post.with(csrf()));
        resultActions.andExpect(status().isOk());
    }

    @Test
    void authenticateUserFail() throws Exception {
        LoginRequest loginRequest = createLoginRequest();
        loginRequest.setUsername("");
        MockHttpServletRequestBuilder post = post("/api/auth/signin").contentType("application/json")
                .content(objectMapper.writeValueAsString(loginRequest));

        ResultActions resultActions = mockMvc.perform(post);
        resultActions.andExpect(status().isBadRequest());
    }

    @Test
    void registerUser() {
    }

    private static LoginRequest createLoginRequest() {
        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setUsername("tudor_user");
        loginRequest.setPassword("password");
        return loginRequest;
    }
}
