import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ENDPOINT } from '../config/endpoint.config';
import { DomSanitizer } from '@angular/platform-browser';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class VideosService {

  constructor(private http: HttpClient, private domSanitizer: DomSanitizer) {
  }

  public getVideos(): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.GET_VIDEOS);
  }

  public uploadVideo(videoToUpload): Observable<any> {
    const formData = new FormData();

    formData.append('video', videoToUpload);

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
}
