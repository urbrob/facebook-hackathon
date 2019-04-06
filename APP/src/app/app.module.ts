import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatBadgeModule} from '@angular/material/badge';
import {MatChipsModule} from '@angular/material/chips';
import {FormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {GraphQLModule} from './graphql.module';
import {HttpClientModule} from '@angular/common/http';
import {AskPageComponent} from './ask-page/ask-page.component';
import {MatButtonModule, MatCardModule, MatInputModule} from '@angular/material';
import {SearchResultsComponent} from './search-results/search-results.component';
import {SearchResultSingleComponent} from './search-result-single/search-result-single.component';
import {QuestionPageComponent} from './question-page/question-page.component';
import {RouterModule, Routes} from '@angular/router';
import {MatIconModule} from '@angular/material/icon';
import {MyProfileComponent} from './my-profile/my-profile.component';

const hashId='3dd339f5-04d8-4dea-ae3b-4c4096eeac94';
const appRoutes: Routes = [
  { path: '', component: AskPageComponent },
  {path: 'question/:id', component: QuestionPageComponent},
  {path:'profile', component:MyProfileComponent}
];
@NgModule({
  declarations: [
    AppComponent,
    AskPageComponent,
    SearchResultsComponent,
    SearchResultSingleComponent,
    QuestionPageComponent,
    MyProfileComponent
  ],
  imports: [
    BrowserModule,
    MatBadgeModule,
    GraphQLModule,
    MatChipsModule,
    FormsModule,
    MatIconModule,
    MatBadgeModule,
    MatCardModule,

    MatInputModule,
    RouterModule.forRoot(
      appRoutes,
      { enableTracing: false } // <-- debugging purposes only
    ),
    MatButtonModule,
    HttpClientModule,
    BrowserAnimationsModule,
  ],

  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
