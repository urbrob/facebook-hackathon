import {Component, OnInit} from '@angular/core';
import gql from 'graphql-tag';
import {Apollo} from 'apollo-angular';
import {UserService} from '../user.service';
import {slide} from '../foldAnimation';

@Component({
  selector: 'app-answer-page',
  templateUrl: './answer-page.component.html',
  styleUrls: ['./answer-page.component.css'],
  animations:[slide]
})
export class AnswerPageComponent implements OnInit {
answerTitle;
answerURL;
index=-1;
question={};
downloaded=false;
questions=[];
filtersSelected=[]
  filters = [
    {name:"length", low:"short", mid:"medium", high:"long"},
    {name:"easiness", low:"for dummies", mid:"medium", high:"sciency"},
    {name:"depth", low:"simple", mid:"medium", high:"complex"}
  ]
  add(a, c){
    let contrary  = c=='low'?'high':'low'
    if (this.filtersSelected.includes(a[c])){
      this.filtersSelected = this.filtersSelected.filter(item => item !== a[c])
    }
    else {
      this.filtersSelected.push(a[c]);
    }
    this.filtersSelected = this.filtersSelected.filter(item => item !== a[contrary])

  }
  constructor(private apollo:Apollo, private user:UserService) { }

  ngOnInit() {
      this.downloadData()
  }
  postAnswer(){
    const isComplex = this.filtersSelected.includes("complex")
    const isScience = this.filtersSelected.includes("sciency")
    const isLong = this.filtersSelected.includes("long")
    this.apollo.mutate({
      mutation:gql`
      mutation createAnswer($title: String!, $url: String!, $questionId: Int!, $hashId: String!, $isComplex: Boolean!, $isScience: Boolean!, $isLong: Boolean!){
        createAnswer(title: $title, url: $url, questionId: $questionId, hashId: $hashId, isComplex:$isComplex, isScience:$isScience, isLong:$isLong){
          answer{
          id
        }
       }
      }`,
      variables:{title:this.answerTitle, url:this.answerURL, questionId:(this.question as any).id, hashId:this.user.hash, isComplex:isComplex, isScience:isScience, isLong:isLong}}).subscribe(({ data }) => {
      console.log('got data', data);
     this.loadNext()


    },(error) => {
      console.log('there was an error sending the query', error);
    });

  }
  downloadData(){
    this.apollo.query({
      query: gql`
          query{
            questions(answersQuestion:2, onlyLocal:${this.user.isLocal}, hashId:"${this.user.hash}"){
              content
              id
              createdAt
             
  }
}
        `,
    }).subscribe(o=>{

      this.questions =(o.data as any).questions;
      this.downloaded=true;
      this.loadNext()
    });
  }
loadNext(){
  this.downloaded=false;
  setTimeout(()=>{
    this.index+=1;
    this.question = this.questions[this.index]
    this.downloaded=true
  }, 500)

}
}
