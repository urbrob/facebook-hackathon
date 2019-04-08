import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  get hash(){
    return localStorage.getItem("hash");
  }
  set hash(s:string){
    localStorage.setItem("hash", s)
  }
  get isLocal():boolean{
    return JSON.parse(localStorage.getItem('isLocal'))
  }
  set isLocal(s:boolean){
    localStorage.setItem('isLocal', JSON.stringify(s))
  }
  toggleLocal(){
    this.isLocal!=this.isLocal;
  }

  constructor() { }
}
