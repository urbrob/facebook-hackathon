import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';
import {fold} from '../foldAnimation';

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
hashId="dc43bc24-4410-4e32-b8e6-6b5ffc2f2570";
  constructor(private route: ActivatedRoute,private apollo: Apollo) { }
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

}}`, variables:{answerId:id, rate:rate, ratingType:type, hashId:this.hashId}}).subscribe(({ data }) => {
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
        }
       }
      }`,
      variables:{title:this.answerTitle, url:this.answerURL, questionId:this.questionId, hashId:this.hashId, isComplex:isComplex, isScience:isScience, isLong:isLong}}).subscribe(({ data }) => {
      console.log('got data', data);

    },(error) => {
      console.log('there was an error sending the query', error);
    });

  }
  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      this.questionId = parseInt(params.get("id"));
    });
    this.apollo.watchQuery({
      query: gql`
          query{
            question(questionId:${this.questionId}){
              content
              id
              createdAt
              answers{
              id
              title
              url
              createdAt
    }
  }
}
        `,
    }).valueChanges.subscribe(o=>{

      this.question =(o.data as any).question;
      this.question['createdAt']=Date.parse(this.question['createdAt']);
      for (let x of this.question['answers']){
        x['createdAt'] = Date.parse(x['createdAt']);
      }
      console.log(this.question)
  this.downloaded=true;
    });

  }

}
