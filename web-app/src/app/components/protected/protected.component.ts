import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { Observable } from 'rxjs';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import DateTimeFormat = Intl.DateTimeFormat;
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-protected',
  templateUrl: './protected.component.html',
  styleUrls: ['./protected.component.scss']
})
export class ProtectedComponent implements OnInit {

  public userContent: string;
  public adminContent: string;

  public selectedFiles: FileList;
  public progressInfos = [];
  public message = '';
  public videoDetail = null;

  public fileInfos: Observable<any>;

  public videoSource;

  constructor(private userService: UserService, private videosService: VideosService, private domSanitizer: DomSanitizer) {
  }

  ngOnInit(): void {
    this.fileInfos = this.videosService.getVideos();
  }

  public selectFiles(event): void {
    this.progressInfos = [];
    this.selectedFiles = event.target.files;
  }

  public uploadFiles(): void {
    this.message = '';

    for (let i = 0; i < this.selectedFiles.length; i++) {
      this.upload(i, this.selectedFiles[i]);
    }
  }

  upload(idx, file): void {
    this.progressInfos[idx] = { value: 'Uploading', fileName: file.name };

    this.videosService.uploadVideo(file).subscribe(
      () => {
        this.fileInfos = this.videosService.getVideos();
        this.progressInfos[idx].value = 'Done';
      },
      err => {
        this.progressInfos[idx].value = 'Error Uploading';
        this.message = 'Could not upload the file:' + file.name;
      });
  }


  public showVideo(id: number): void {
    this.videosService.getVideo(id).subscribe(
      (response: any) => {
        this.videoDetail = response;
      }
    );
    this.videosService.streamVideo(id).subscribe(
      (resp) => {
        console.log(resp);
        this.videoSource = resp;
      }, error => {
        console.log(error);
        console.log('error streaming video');
      }
    );
  }
}
