import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-search-result-single',
  templateUrl: './search-result-single.component.html',
  styleUrls: ['./search-result-single.component.css'],

})
export class SearchResultSingleComponent implements OnInit {
  @Input() result;
  constructor() { }

  ngOnInit() {
  }


}
