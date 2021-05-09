import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {

  public selectedFiles: FileList;
  public progressInfos = [];
  public message = '';


  constructor(private userService: UserService, private videosService: VideosService) {
  }

  ngOnInit(): void {
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
        this.progressInfos[idx].value = 'Done';
      },
      err => {
        this.progressInfos[idx].value = 'Error Uploading';
        this.message = 'Could not upload the file:' + file.name;
      });
  }
}
