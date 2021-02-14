import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ENDPOINT } from '../config/endpoint.config';

@Injectable({
  providedIn: 'root'
})
export class VideosService {

  constructor(private http: HttpClient) {
  }

  public getVideos(): Observable<any> {
    return this.http.get(ENDPOINT.VIDEOS_API.GET_VIDEOS);
  }

  public uploadVideo(videoToUpload): Observable<any> {
    const formData = new FormData();

    formData.append('video', videoToUpload);

    return this.http.post(ENDPOINT.VIDEOS_API.UPLOAD_ONE, formData);
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
    return this.http.get(ENDPOINT.VIDEOS_API.STREAM(id));
  }
}
