export interface Task {
  _id: string;
  name: string;
  description: string;
  dataset: string;
  type: string;
  trained: boolean;
  accuracy: number;
  action: boolean;
  supervisor: boolean;
}
