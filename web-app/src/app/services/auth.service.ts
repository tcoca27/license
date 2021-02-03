import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ENDPOINT } from '../config/endpoint.config';
import { Observable } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private http: HttpClient) {
  }

  public login(credentials): Observable<any> {
    return this.http.post(ENDPOINT.AUTH_API.SIGNIN, {
      username: credentials.username,
      password: credentials.password
    }, httpOptions);
  }

  public register(user): Observable<any> {
    return this.http.post(ENDPOINT.AUTH_API.SIGNUP, {
      username: user.username,
      password: user.password,
      email: user.email
    }, httpOptions);
  }
}
