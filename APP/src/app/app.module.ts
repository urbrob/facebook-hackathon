import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {MatButtonModule, MatCardModule, MatInputModule, MatProgressSpinnerModule, MatRippleModule} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatBadgeModule} from '@angular/material/badge';
import {MatChipsModule} from '@angular/material/chips';
import {FormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import {GraphQLModule} from './graphql.module';
import {HttpClientModule} from '@angular/common/http';
import {AskPageComponent} from './ask-page/ask-page.component';
import {SearchResultsComponent} from './search-results/search-results.component';
import {SearchResultSingleComponent} from './search-result-single/search-result-single.component';
import {QuestionPageComponent} from './question-page/question-page.component';
import {RouterModule, Routes} from '@angular/router';
import {MatIconModule} from '@angular/material/icon';
import {MyProfileComponent} from './my-profile/my-profile.component';
import {MatListModule} from '@angular/material/list';
import {LoginComponent} from './login/login.component';
import {BrowseQuestionsPageComponent} from './browse-questions-page/browse-questions-page.component';
import {AnswerPageComponent} from './answer-page/answer-page.component';
import {MyGroupsPageComponent} from './my-groups-page/my-groups-page.component';

const hashId='3dd339f5-04d8-4dea-ae3b-4c4096eeac94';
const appRoutes: Routes = [
  { path: '', component: AskPageComponent },
  {path: 'question/:id', component: QuestionPageComponent},
  {path:'profile', component:MyProfileComponent},
  {path:'login', component:LoginComponent},
  {path:'questions', component:BrowseQuestionsPageComponent},
  {path:'answer', component:AnswerPageComponent},
  {path:'myGroups', component:MyGroupsPageComponent}

];
@NgModule({
  declarations: [
    AppComponent,
    AskPageComponent,
    SearchResultsComponent,
    SearchResultSingleComponent,
    QuestionPageComponent,
    MyProfileComponent,
    LoginComponent,
    BrowseQuestionsPageComponent,
    AnswerPageComponent,
    MyGroupsPageComponent
  ],
  imports: [
    BrowserModule,
    MatBadgeModule,
    GraphQLModule,
    MatChipsModule,
    MatListModule,
    FormsModule,

   MatProgressSpinnerModule,
    MatIconModule,
    MatBadgeModule,
    MatCardModule,
MatRippleModule,
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
