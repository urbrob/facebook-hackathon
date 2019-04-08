import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';
import {fold} from '../foldAnimation';
import {UserService} from '../user.service';

@Component({
  selector: 'app-question-page',
  templateUrl: './question-page.component.html',
  styleUrls: ['./question-page.component.css'],
  animations: [
    fold
  ]
})
export class QuestionPageComponent implements OnInit {
  answerTitle;
  answerURL;
  answerFilters;


  questionId: number;
  question: object;
  downloaded=false;
  markAsVisited(x){
    x.isVisited=true;
  }
  constructor(private route: ActivatedRoute,private apollo: Apollo,private user:UserService) { }
  vote(id, rate, type){
    this.apollo.mutate({
      mutation: gql`mutation createRating($answerId: Int!, $rate: Boolean!, $ratingType: RatingTypes!, $hashId: String!) {
  createRating(answerId: $answerId, rate: $rate, ratingType: $ratingType, hashId: $hashId)
{
  rating{
    rate
    ratingType
    answer{
      title
    }
  }

}}`, variables:{answerId:id, rate:rate, ratingType:type, hashId:this.user.hash}}).subscribe(({ data }) => {
      console.log('got data', data);
    },(error) => {
      console.log('there was an error sending the query', error);
    });
  }
  filtersSelected=[];
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
               isLong
                isComplex
                helpfulCount
                isScience
              title
              url(userHash:"${this.user.hash}")
              isVisited(userHash:"${this.user.hash}")
              createdAt
        }
       }
      }`,
      variables:{title:this.answerTitle, url:this.answerURL, questionId:this.questionId, hashId:this.user.hash, isComplex:isComplex, isScience:isScience, isLong:isLong}}).subscribe(({ data }) => {
      console.log('got data', data);
      let a = data.createAnswer.answer;
      (this.question as any).answers.push(a)
     // this.downloadData()


    },(error) => {
      console.log('there was an error sending the query', error);
    });

  }
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.questionId = parseInt(params.get("id"));
      this.downloadData()
    });


  }
  markAsHelpful(x){
    x.helpfulCount+=1;
  }
  downloadData(){
    this.apollo.query({
      query: gql`
          query{
            question(questionId:${this.questionId}){
              content
              id
              
              createdAt
              answers(hashId:"${this.user.hash}", onlyLocal:${this.user.isLocal}){
              id
               isLong
                isComplex
                helpfulCount
                isScience
              title
              url(userHash:"${this.user.hash}")
              isVisited(userHash:"${this.user.hash}")
              createdAt
    }
  }
}
        `,
    }).subscribe(o=>{
      console.log(o.data)

      this.question =(o.data as any).question;

      console.log(this.question)
      this.downloaded=true;
    });
  }

}
