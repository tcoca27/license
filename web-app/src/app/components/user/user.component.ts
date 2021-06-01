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

  constructor(private userService: UserService, private videosService: VideosService) {
  }

  public selectedFiles: FileList;
  public progressInfos = [];
  public message = '';
  public attColor: string;
  public defColor: string;

  static getHSL(color: string): string[] {
    const colors: string = color.split('(')[1];
    const tokens = colors.split(',');
    const h = tokens[0];
    const s = tokens[1].split('%')[0];
    const l = tokens[2].split('%')[0];
    return [h, s, l];
  }

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
      this.upload(i, this.selectedFiles[i], UserComponent.getHSL(this.attColor), UserComponent.getHSL(this.defColor));
    }
  }

  public upload(idx, file, attColor, defColor): void {
    this.progressInfos[idx] = { value: 'Uploading', fileName: file.name };

    this.videosService.uploadVideo(file, attColor, defColor).subscribe(
      () => {
        this.progressInfos[idx].value = 'Done';
      },
      err => {
        this.progressInfos[idx].value = 'Error Uploading';
        this.message = 'Could not upload the file:' + file.name;
      });
  }

  public attColorChange(color: string): void {
    this.attColor = color;
  }

  public defColorChange(color: string): void {
    this.defColor = color;
  }
}
