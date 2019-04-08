import {Component} from '@angular/core';
import {UserService} from './user.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-root',

  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'APP';
  get mode(){
    return this.User.isLocal?"Groups":"Global";
  }
  switch(){
    if (!this.User.isLocal)
    this.User.isLocal=true;
    else
      this.User.isLocal=false;
    location.reload();
  }
  constructor(private User:UserService, private r:Router){}
  logout(){
    this.User.hash='';
    this.r.navigate(['/login'])
  }
}
