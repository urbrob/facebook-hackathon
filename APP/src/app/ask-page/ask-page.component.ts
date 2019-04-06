import {Component, OnInit} from '@angular/core';
import {fold} from '../foldAnimation';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';

declare var Chance:any;
@Component({
  selector: 'app-ask-page',
  templateUrl: './ask-page.component.html',
  styleUrls: ['./ask-page.component.css'],
  animations: [
  fold
  ]
})
export class AskPageComponent implements OnInit {
  hashId="dc43bc24-4410-4e32-b8e6-6b5ffc2f2570";
  topStrings = [
    //"Hi! Does anyone know ",
    "Hi! How can I learn about",
    "Hi! I am looking for ",
    "Hi! I need something about",
    "Hello, I want to know about",
//    "I write to ask for materials about",
    "I want to learn about",
    "I would like to know more about"];
  topString:string = '';
  search: string = '';
  filtersSelected=[];
  filters = [
    {name:"length", low:"short", mid:"medium", high:"long"},
    {name:"easiness", low:"for dummies", mid:"medium", high:"sciency"},
    {name:"depth", low:"simple", mid:"medium", high:"complex"}
  ]
  chance: any;
  constructor(private apollo: Apollo) {
  }
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
  ngOnInit() {
    this.chance  = new Chance();
    this.topString = this.chance.pickone(this.topStrings);
  }
  postQuestion(){
    this.apollo.mutate({
      mutation:gql`
        mutation createQuestion($hashId: String!, $question: String!){
        createQuestion(hashId: $hashId, question: $question){
       question{
            id
            }}
}
      `, variables:{hashId:this.hashId, question:this.search}
    }).subscribe(({ data }) => {
      console.log('got data', data);
    },(error) => {
      console.log('there was an error sending the query', error);
    });
    console.log("XDDD");
  }

}
