import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ENDPOINT } from '../config/endpoint.config';
import { DomSanitizer } from '@angular/platform-browser';
import { map } from 'rxjs/operators';
import { TokenStorageService } from './token-storage.service';

@Injectable({
  providedIn: 'root'
})
export class VideosService {

  constructor(private http: HttpClient, private domSanitizer: DomSanitizer, private tokenStorageService: TokenStorageService) {
  }

  public getVideos(): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.GET_VIDEOS);
  }

  public uploadVideo(videoToUpload, attColor, defColor): Observable<any> {
    const formData = new FormData();

    formData.append('video', videoToUpload);
    formData.append('attColor', attColor);
    formData.append('defColor', defColor);

    return this.http.post(ENDPOINT.VIDEOS_API.UPLOAD_ONE, formData, {
      reportProgress: true,
      responseType: 'json'
    });
  }

  public uploadVideos(videosToUpload): Observable<any> {
    return this.http.post(ENDPOINT.VIDEOS_API.UPLOAD_MULTIPLE, {
      video: videosToUpload
    });
  }

  public getVideo(id: number): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.GET_ONE(id));
  }

  public streamVideo(id: number): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.STREAM(id), {
      responseType: 'blob',
    }).pipe(map(e => this.domSanitizer.bypassSecurityTrustResourceUrl(URL.createObjectURL(e))));
  }

  public getMyVideos(): Observable<any> {
    console.log(ENDPOINT.VIDEOS_API.MY);
    return this.http.get(ENDPOINT.VIDEOS_API.MY);
  }

  public getResults(id: number): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.RESULTS(id));
  }

  public deleteVideo(id: number): Observable<any> {
    return this.http.delete(ENDPOINT.VIDEOS_API.STREAM(id));
  }

  public deleteUser(username: string): Observable<any> {
    return this.http.delete(ENDPOINT.USER_API.USER(username));
  }

  public isCurrentUser(username: string): boolean {
    return this.tokenStorageService.getUser().username === username;
  }

  public paintSegmentation(id: number): Observable<any> {
    const headers = new HttpHeaders({
      Accept: 'application/zip, */*'
    });
    return this.http.get(ENDPOINT.VIDEOS_API.PAINT(id), { responseType: 'blob', observe: 'response', headers });
  }

  public personsDetection(id: number): Observable<any> {
    const headers = new HttpHeaders({
      Accept: 'application/zip, */*'
    });
    return this.http.get(ENDPOINT.VIDEOS_API.PERSONS(id), { responseType: 'blob', observe: 'response', headers });
  }

  public findSide(id: number): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.SIDE(id));
  }
}
