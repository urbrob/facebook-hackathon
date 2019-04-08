import {Component, Input, OnInit} from '@angular/core';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';
import {UserService} from '../user.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {
  @Input()
  selectedFilters;
  @Input()
  set searchString(s: string){
    if (s.length>2) {
      this.DoSearch(s,this.selectedFilters);
    }
    else{
      this.resultsList=[];
    }
  }

  resultsList = [];
  constructor(private apollo: Apollo, private user:UserService) { }

  ngOnInit() {
  }

  DoSearch(s: string, filtersSelected) {
    const isComplex = filtersSelected.includes("complex")?true:filtersSelected.includes("simple")?true:null;
    const isScience = filtersSelected.includes("sciency")?true:filtersSelected.includes("for dummies")?true:null;
    const isLong = filtersSelected.includes("long")?true:filtersSelected.includes("short")?true:null;
    let s2  = '';
    if (isLong!=null){
      s2+=`isLong:${isLong},`;
    }
    if (isScience!=null){
      s2+=`isScience: ${isScience},`;
    }
    if (isComplex!=null){
      s2+=`isComplex: ${isComplex},`;
    }
    if (s2.length>0) {
      s2 = s2.substring(0, s2.length - 0);
      console.log(s2)
    }

    this.apollo.watchQuery({
      query: gql`
          query{
            questions(answersQuestion:999, question:"${s}", onlyLocal:${this.user.isLocal}, hashId:"${this.user.hash}"){
              content
              id
              answers(${s2} onlyLocal:${this.user.isLocal}, hashId:"${this.user.hash}"){
                id
                title
                url
                createdAt
                isLong
                isComplex
                isScience
    }
  }
}
        `,
    }).valueChanges.subscribe(o=>{
      console.log(o)
      this.resultsList=[];
      for (let x of o.data['questions']){
        for (let a of x.answers){
          this.resultsList.push({answer:a, question:x});
        }
      }
      console.log(this.resultsList)

    });
  }

}
