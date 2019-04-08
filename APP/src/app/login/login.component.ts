import {Component, OnInit} from '@angular/core';
import {Apollo} from 'apollo-angular';
import gql from 'graphql-tag';
import {UserService} from '../user.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
login;
pass;
  constructor(private apollo:Apollo, private user:UserService,private router:Router) { }

  ngOnInit() {
  }
  Register(){
    this.apollo.mutate({mutation:gql`
    mutation registerUser($email: String!, $password: String!){
  registerUser(email: $email, password: $password){
    hashId
  
  }
}`, variables:{email:this.login, password:this.pass}}).subscribe(d=>{
     this.user.hash = (d.data as any).registerUser.hashId;
      this.router.navigate(['/'])
    })
  }
  LoginMethod(){
    this.apollo.mutate({mutation:gql`
    mutation loginUser($email: String!, $password: String!){
  loginUser(email: $email, password: $password){
    hashId
    inGroup
  }
}
    `, variables:{email:this.login, password:this.pass}}).subscribe(d=>{
    this.user.hash = (d.data as any).loginUser.hashId;
    this.router.navigate(['/'])
    }
  );


}}
