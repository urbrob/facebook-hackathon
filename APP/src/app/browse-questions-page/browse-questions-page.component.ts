import {Component, OnInit} from '@angular/core';
import {Apollo} from 'apollo-angular';
import {UserService} from '../user.service';
import gql from 'graphql-tag';

@Component({
  selector: 'app-browse-questions-page',
  templateUrl: './browse-questions-page.component.html',
  styleUrls: ['./browse-questions-page.component.css']
})
export class BrowseQuestionsPageComponent implements OnInit {

  questions=[];
  downloaded=false;
  constructor(private apollo:Apollo, private user:UserService) { }

  ngOnInit() {
    this.questions=[]

    this.apollo.watchQuery({
      query: gql`
          query{
            questions(answersQuestion:999, onlyLocal:${this.user.isLocal}, hashId:"${this.user.hash}"){
              content
              id
              createdAt
             answersCount(onlyLocal:${this.user.isLocal}, hashId:"${this.user.hash}")
  }
}

        `,
    }).valueChanges.subscribe(o=>{
      console.log(o);
      this.downloaded=true;
      this.questions = (o.data as any).questions;


    });
  }
  }

