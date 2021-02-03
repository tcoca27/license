import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ENDPOINT } from '../config/endpoint.config';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) {
  }

  public getPublicContent(): Observable<any> {
    return this.http.get(ENDPOINT.TESP_API.ALL, { responseType: 'text' });
  }

  public getUserContent(): Observable<any> {
    return this.http.get(ENDPOINT.TESP_API.USER, { responseType: 'text' });
  }

  public getAdminContent(): Observable<any> {
    return this.http.get(ENDPOINT.TESP_API.ADMIN, { responseType: 'text' });
  }
}
