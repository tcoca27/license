import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { VideosService } from '../../services/videos.service';
import { ColorEnum } from '../../basketball/color-enum';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss']
})
export class UserComponent implements OnInit {

  constructor(private userService: UserService, private videosService: VideosService) {
    this.keys = Object.keys(this.colors).filter(k => isNaN(Number(k)));
    console.log(this.keys);
  }

  public selectedFiles: FileList;
  public progressInfos = [];
  public message = '';
  public attColor = ColorEnum.BLACK;
  public defColor = ColorEnum.WHITE;
  public colors = ColorEnum;
  public keys;

  ngOnInit(): void {
  }

  public selectFiles(event): void {
    this.progressInfos = [];
    this.selectedFiles = event.target.files;
  }

  public uploadFiles(): void {
    this.message = '';

    console.log('here');
    if (!this.selectedFiles || !this.defColor || !this.attColor) {
      this.message = 'Please fill in all the fields.';
      return;
    }

    for (let i = 0; i < this.selectedFiles.length; i++) {
      this.upload(i, this.selectedFiles[i]);
    }
  }

  public upload(idx, file): void {
    this.progressInfos[idx] = { value: 'Uploading', fileName: file.name };

    this.videosService.uploadVideo(file, this.attColor, this.defColor).subscribe(
      () => {
        this.progressInfos[idx].value = 'Done';
      },
      err => {
        this.progressInfos[idx].value = 'Error Uploading';
        this.message = 'Could not upload the file:' + file.name;
      });
  }
}
