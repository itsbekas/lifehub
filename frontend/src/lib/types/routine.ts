export interface Task {
  id: string;
  title: string;
  due: string;
}

export interface TaskList {
  id: string;
  title: string;
  tasks: Task[];
}