import {Component, OnInit} from '@angular/core';
import {Apollo} from 'apollo-angular';
import {UserService} from '../user.service';
import gql from 'graphql-tag';
import {slide} from '../foldAnimation';

@Component({
  selector: 'app-my-groups-page',
  templateUrl: './my-groups-page.component.html',
  styleUrls: ['./my-groups-page.component.css'],
  animations:[slide]
})
export class MyGroupsPageComponent implements OnInit {
  groups=[]
  groupName;
  downloaded=false;
  makeGroup(){
    this.apollo.mutate({
      mutation:gql`
      mutation addGroup($group: String!, $hashId: String!){
  addGroup(group: $group, hashId: $hashId){
    group{
      id
      name
    }
  }
}
      `
    ,variables:{group:this.groupName, hashId:this.user.hash}}).subscribe(d=>{
      this.groups.push({name:d.data.addGroup.group.name, id:d.data.addGroup.group.id})
    })
  }
  constructor(private apollo:Apollo, private user:UserService) { }
  sendInvite(g){
    this.apollo.mutate({mutation:gql`
      mutation addToGroup($email: String!, $groupId: Int!){
  addToGroup(groupId: $groupId, email: $email){
    status
  }
}
    
    `, variables:{email:g.mail, groupId:g.id}}).subscribe(d=>{
      console.log(d)
    })
  }
  ngOnInit() {
    this.apollo.watchQuery({query:gql`
        query{
        userGroups(hashId: "${this.user.hash}"){
          id
          name
          
        }
        }
    
    `}).valueChanges.subscribe(d=>{
      this.groups = (d.data as any).userGroups;
      for (let g of this.groups){
        g.mail = ''
      }
      console.log(this.groups)
      this.downloaded=true;
    })
  }


}
