import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'idFilter'
})
export class IdFilterPipe implements PipeTransform {
  transform(value: any, id: any): any {
    if (value._id === id) {
      return value.message;
    }
  }
}
