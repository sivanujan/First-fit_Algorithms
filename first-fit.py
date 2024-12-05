import tkinter as tk
from tkinter import messagebox

def first_fit(blocks, process_size):
    allocation = -1
    for i in range(len(blocks)):
        if blocks[i]['remaining_size'] >= process_size:
            allocation = i
            blocks[i]['remaining_size'] -= process_size  # Deduct process size from remaining space
            blocks[i]['allocated_processes'].append(process_size)  # Store allocated process size in the block
            break
    return allocation, blocks

class MemoryAllocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("First Fit Memory Allocation")

    
        self.instructions = tk.Label(root, text="Enter the number of blocks and their sizes.", font=('Arial', 12))
        self.instructions.pack(pady=10)

    
        self.num_blocks_label = tk.Label(root, text="Number of Memory Blocks:")
        self.num_blocks_label.pack()
        self.num_blocks_entry = tk.Entry(root)
        self.num_blocks_entry.pack(pady=5)

 
        self.blocks_label = tk.Label(root, text="Enter block sizes (comma-separated):")
        self.blocks_label.pack()
        self.blocks_entry = tk.Entry(root)
        self.blocks_entry.pack(pady=5)

    
        self.start_button = tk.Button(root, text="Setup Blocks and Start Process Allocation", command=self.setup_blocks)
        self.start_button.pack(pady=20)

     
        self.num_processes_label = tk.Label(root, text="Enter the number of Processes:")
        self.num_processes_label.pack(pady=5)
        self.num_processes_entry = tk.Entry(root)
        self.num_processes_entry.pack(pady=5)

      
        self.process_size_label = tk.Label(root, text="Enter process size:")
        self.process_size_label.pack(pady=5)
        self.process_size_entry = tk.Entry(root)
        self.process_size_entry.pack(pady=5)


        self.allocate_button = tk.Button(root, text="Allocate Process", command=self.allocate_process, state="disabled")
        self.allocate_button.pack(pady=10)

      
        self.result_label = tk.Label(root, text="", font=('Arial', 12))
        self.result_label.pack(pady=10)

      
        self.blocks = []
        self.num_processes = 0
        self.process_count = 0
        self.allocation = []
        self.processes = []  

    def setup_blocks(self):
        try:
            num_blocks = int(self.num_blocks_entry.get())
            if num_blocks <= 0:
                messagebox.showerror("Input Error", "Number of blocks must be greater than zero.")
                return

            blocks = self.blocks_entry.get().split(',')
            if len(blocks) != num_blocks:
                messagebox.showerror("Input Error", "Number of block sizes does not match the number of blocks entered.")
                return
            
            blocks = [int(block.strip()) for block in blocks if block.strip().isdigit()]
            if len(blocks) != num_blocks:
                messagebox.showerror("Input Error", "Please enter valid numeric block sizes.")
                return

         
            self.blocks = [{'size': block, 'remaining_size': block, 'allocated_processes': []} for block in blocks]
            self.allocation = [-1] * len(blocks)
            self.num_processes = int(self.num_processes_entry.get())
            if self.num_processes <= 0:
                messagebox.showerror("Input Error", "Number of processes must be greater than zero.")
                return

        
            self.process_count = 0
            self.processes = []

      
            self.result_label.config(text="Blocks setup completed. Now, enter process sizes one by one.")
            self.allocate_button.config(state="normal")
            self.process_size_entry.config(state="normal")
            self.process_size_label.config(state="normal")
            self.start_button.config(state="disabled") 

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for blocks and processes.")

    def allocate_process(self):
        try:
           
            process_size = int(self.process_size_entry.get())
            if process_size <= 0:
                messagebox.showerror("Input Error", "Process size must be greater than zero.")
                return

           
            self.processes.append({"process_number": self.process_count + 1, "size": process_size})

       
            allocation, self.blocks = first_fit(self.blocks.copy(), process_size)

        
            result_text = ""
            if allocation == -1:
                result_text = f"Process {self.process_count + 1} (Size: {process_size}) could not be allocated.\n"
            else:
                result_text = f"Process {self.process_count + 1} (Size: {process_size}) allocated to Block {allocation + 1}.\n"
                self.allocation[allocation] = process_size

            result_text += "\nCurrent Block Status:\n"
            for i, block in enumerate(self.blocks):
                allocated_processes = ', '.join(map(str, block['allocated_processes']))
                result_text += f"Block {i + 1}: {'Allocated' if len(block['allocated_processes']) > 0 else 'Free'} (Remaining Size: {block['remaining_size']})"
                if len(block['allocated_processes']) > 0:
                    result_text += f" | Allocated Processes: {allocated_processes}\n"
                else:
                    result_text += "\n"

            free_blocks = [block for block in self.blocks if block['remaining_size'] > 0]
           

            self.result_label.config(text=result_text)
            self.process_size_entry.delete(0, tk.END)

            self.process_count += 1
            if self.process_count >= self.num_processes:
                self.allocate_button.config(state="disabled")
                self.show_final_allocation()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for process size.")

    def show_final_allocation(self):
        final_summary = "\nFinal Memory Allocation Summary:\n"
        for process in self.processes:
            process_number = process['process_number']
            process_size = process['size']
            allocated_block = None

           
            for i, block in enumerate(self.blocks):
                if process_size in block['allocated_processes']:
                    allocated_block = i + 1  

            if allocated_block:
                final_summary += f"Process {process_number} (Size: {process_size}) allocated to Block {allocated_block}.\n"
            else:
                final_summary += f"Process {process_number} (Size: {process_size}) could not be allocated.\n"
        
        final_summary += "\nFinal Block Status:\n"
        for i, block in enumerate(self.blocks):
            allocated_processes = ', '.join(map(str, block['allocated_processes']))
            final_summary += f"Block {i + 1}: {'Allocated' if len(block['allocated_processes']) > 0 else 'Free'} (Remaining Size: {block['remaining_size']})"
            if len(block['allocated_processes']) > 0:
                final_summary += f" | Allocated Processes: {allocated_processes}\n"
            else:
                final_summary += "\n"
        
        self.result_label.config(text=final_summary)


root = tk.Tk()
app = MemoryAllocationApp(root)
root.mainloop()














