import {Component, OnInit} from '@angular/core';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';
import {UserService} from '../user.service';

@Component({
  selector: 'app-my-profile',
  templateUrl: './my-profile.component.html',
  styleUrls: ['./my-profile.component.css']
})
export class MyProfileComponent implements OnInit {
  questions=[];
  downloaded=false;
  constructor(private apollo:Apollo, private user:UserService) { }

  ngOnInit() {
  this.apollo.watchQuery({query:gql`
  query{
  userQuestions(hashId: "${this.user.hash}"){
    id
    content
    answersCount(hashId: "${this.user.hash}", onlyLocal:${this.user.isLocal})
  }
}
  `}).valueChanges.subscribe(d=>{
    this.downloaded=true;
    this.questions =( d.data as any).userQuestions;
  })
  }

}
