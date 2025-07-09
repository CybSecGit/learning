# Learning Plan: GPT-2 for Log Anomaly Detection
## *Or: How to Teach a Language Model to Be Your Paranoid Security Analyst*

> "The best way to find weird stuff in your logs is to train an AI that thinks normal logs are Shakespeare and anomalies are... well, whatever this is." - Anonymous SRE who discovered cryptominers at 3 AM

Welcome to the world where we turn OpenAI's GPT-2 (yes, the one that was "too dangerous to release") into your personal log anomaly detective. By the end of this journey, you'll have built a system that can spot weird stuff in your logs faster than you can say "unauthorized access attempt."

## Why GPT-2 for Log Analysis?
### *Spoiler: It's Actually Brilliant*

**The Traditional Approach** (aka "The Pain"):
- Regex patterns that break when someone adds a space
- Rule-based systems with 10,000 rules that still miss the obvious
- Statistical models that think every Tuesday is an anomaly
- SOC analysts drinking their 8th coffee while staring at dashboards

**The GPT-2 Approach** (aka "The Gain"):
- Learns what "normal" looks like by reading millions of log lines
- Spots anomalies by detecting "this doesn't look like the usual stuff"
- No rules to maintain (the model maintains itself... mostly)
- Works on any log format (Apache, syslog, custom nonsense from that one developer)

**Real Talk**: GPT-2 understands context. When it sees:
```
2024-01-15 10:00:01 INFO User admin logged in from 192.168.1.100
2024-01-15 10:00:02 INFO User admin accessed /dashboard
2024-01-15 10:00:03 INFO User admin logged in from 45.123.456.789
2024-01-15 10:00:04 INFO User admin deleted entire production database
```

It knows something's fishy about lines 3-4, not because of rules, but because it learned that admins don't usually teleport across continents in 1 second or casually delete production.

## Prerequisites
### *What You Need to Know (Or Learn Really Fast)*

1. **Python Proficiency** - You should be able to:
   - Write functions without googling syntax every 5 minutes
   - Understand async/await (we're processing logs in real-time)
   - Not panic when you see decorators

2. **Basic ML Understanding** - You should know:
   - What a neural network is (boxes connected by lines that do math)
   - What training vs inference means
   - Why GPUs make things go brrrr

3. **Log File Experience** - You should have:
   - Seen a log file before (and survived)
   - Basic understanding of log levels (INFO good, ERROR bad, CRITICAL very bad)
   - Patience for reading thousands of lines of timestamps

4. **Command Line Comfort** - You should be able to:
   - Navigate directories without a GUI
   - Run Python scripts
   - Not accidentally delete system files

## The Learning Path
### *From "What's GPT-2?" to "My Logs Are Sentient Now"*

### Phase 1: Understanding the Problem Space (Week 1)
#### *"Why Are We Doing This Again?"*

**Day 1-2: The Log Analysis Nightmare**

First, let's understand why log analysis makes people cry:

```python
# Traditional approach (the suffering)
def find_anomalies_with_regex(log_file):
    """
    This function will haunt your dreams.
    """
    patterns = [
        r"failed login.*root",  # Catches some attacks
        r"error.*database",     # Catches some errors
        r"suspicious.*activity", # Catches nothing because attackers don't log "suspicious activity"
        # ... 9,997 more patterns
    ]
    
    # Still misses the clever attacks
    # Still has false positives
    # Still makes you question your career choices
```

**What You'll Learn**:
- Why rule-based systems fail (spoiler: attackers read your rules)
- Common log formats and their quirks
- What anomalies actually look like in the wild
- How to set up a log generation lab

**Hands-On Exercise**: Build a Log Chaos Generator
```python
import random
import datetime
import json

class LogChaosGenerator:
    """
    Generates realistic logs with hidden anomalies.
    Like a CTF challenge, but for your future self.
    """
    
    def __init__(self):
        self.users = ["admin", "user1", "user2", "definitely_not_a_hacker"]
        self.ips = ["192.168.1.100", "10.0.0.50", "8.8.8.8", "127.0.0.1"]
        self.actions = ["login", "logout", "access_file", "drop_table_users"]
        
    def generate_normal_log(self):
        """Generate a boring, normal log entry."""
        timestamp = datetime.datetime.now().isoformat()
        user = random.choice(self.users[:-1])  # Exclude the hacker
        ip = random.choice(self.ips[:-2])      # Exclude suspicious IPs
        action = random.choice(self.actions[:-1])  # Exclude bad actions
        
        return f"{timestamp} INFO {user} from {ip} performed {action}"
    
    def generate_anomaly(self):
        """Generate something fishy."""
        timestamp = datetime.datetime.now().isoformat()
        
        anomaly_types = [
            # Suspicious user
            lambda: f"{timestamp} INFO {self.users[-1]} from {random.choice(self.ips)} performed {random.choice(self.actions)}",
            
            # Suspicious IP
            lambda: f"{timestamp} INFO {random.choice(self.users)} from {self.ips[-1]} performed {random.choice(self.actions)}",
            
            # Suspicious action
            lambda: f"{timestamp} INFO {random.choice(self.users)} from {random.choice(self.ips)} performed {self.actions[-1]}",
            
            # Time anomaly (logs from the future!)
            lambda: f"{(datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()} INFO user1 from 192.168.1.100 performed login",
            
            # Format anomaly
            lambda: f"{timestamp} CRITICAL System32 has been deleted. Have a nice day!",
        ]
        
        return random.choice(anomaly_types)()
    
    def generate_dataset(self, num_logs=10000, anomaly_rate=0.01):
        """
        Generate a dataset with hidden anomalies.
        Like Where's Waldo, but Waldo is trying to steal your data.
        """
        logs = []
        for i in range(num_logs):
            if random.random() < anomaly_rate:
                logs.append({"log": self.generate_anomaly(), "label": "anomaly"})
            else:
                logs.append({"log": self.generate_normal_log(), "label": "normal"})
        
        return logs

# Generate your training data
generator = LogChaosGenerator()
dataset = generator.generate_dataset(num_logs=100000, anomaly_rate=0.01)

# Save it
with open("log_dataset.jsonl", "w") as f:
    for entry in dataset:
        f.write(json.dumps(entry) + "\n")

print(f"Generated {len(dataset)} logs with {sum(1 for d in dataset if d['label'] == 'anomaly')} anomalies")
print("Good luck finding them without AI!")
```

**Day 3-4: GPT-2 Crash Course**

Time to understand our weapon of choice:

```python
# Your first taste of GPT-2
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained model (warning: this downloads ~500MB)
model_name = "gpt2"  # Start small, dream big
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Let's see what GPT-2 thinks about logs
def gpt2_understands_logs():
    """
    Spoiler: It doesn't... yet.
    """
    log_line = "2024-01-15 10:00:00 INFO User admin logged in from "
    
    # Tokenize
    inputs = tokenizer(log_line, return_tensors="pt")
    
    # Generate completion
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids, 
            max_length=50,
            num_return_sequences=1,
            temperature=0.7
        )
    
    completion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"GPT-2 thinks the log continues: {completion}")
    # Probably generates something about Paris or unicorns
    # This is why we need to train it!

gpt2_understands_logs()
```

**What You'll Learn**:
- How transformers work (the ML kind, not Optimus Prime)
- Tokenization (turning text into numbers)
- Why perplexity matters (confused model = anomaly detected)
- The difference between GPT-2 sizes (small, medium, large, "my-GPU-is-crying")

### Phase 2: Building Your First Anomaly Detector (Week 2-3)
#### *"It's Alive! (And It Thinks Everything Is Weird)"*

**Day 5-7: Data Preparation Pipeline**

First rule of ML: Garbage in, garbage out. Let's build a non-garbage pipeline:

```python
import re
from datetime import datetime
import pandas as pd
from typing import List, Dict, Tuple

class LogPreprocessor:
    """
    Turns your messy logs into GPT-2 food.
    Like a chef, but for data.
    """
    
    def __init__(self):
        # Common log patterns (add more for your logs)
        self.patterns = {
            'syslog': re.compile(
                r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
                r'(?P<hostname>\S+)\s+'
                r'(?P<process>\S+?):\s+'
                r'(?P<message>.*)'
            ),
            'apache': re.compile(
                r'(?P<ip>\S+)\s+\S+\s+\S+\s+'
                r'\[(?P<timestamp>[^\]]+)\]\s+'
                r'"(?P<request>[^"]+)"\s+'
                r'(?P<status>\d+)\s+'
                r'(?P<size>\S+)'
            ),
            'custom': re.compile(
                r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
                r'(?P<level>\w+)\s+'
                r'(?P<message>.*)'
            )
        }
        
        # Tokenization settings
        self.max_length = 512  # GPT-2's context window
        self.preserve_fields = ['timestamp', 'level', 'message']
        
    def parse_log(self, log_line: str, log_format: str = 'custom') -> Dict:
        """
        Parse a log line into structured data.
        Returns None if parsing fails (which means it's probably an anomaly!)
        """
        pattern = self.patterns.get(log_format)
        if not pattern:
            return {"raw": log_line, "parsed": False}
        
        match = pattern.match(log_line.strip())
        if not match:
            return {"raw": log_line, "parsed": False}
        
        return {
            "raw": log_line,
            "parsed": True,
            **match.groupdict()
        }
    
    def normalize_log(self, parsed_log: Dict) -> str:
        """
        Convert parsed log to GPT-2 friendly format.
        We keep some structure to help the model learn patterns.
        """
        if not parsed_log.get("parsed"):
            # Unparseable logs are suspicious by default
            return f"<ANOMALY> {parsed_log['raw']}"
        
        # Create a normalized representation
        parts = []
        
        # Normalize timestamp to relative time
        if 'timestamp' in parsed_log:
            parts.append("<TIME>")  # Abstract timestamp
        
        # Keep level if present
        if 'level' in parsed_log:
            parts.append(f"<{parsed_log['level']}>")
        
        # Process message
        if 'message' in parsed_log:
            # Normalize IPs (privacy + generalization)
            message = re.sub(r'\d+\.\d+\.\d+\.\d+', '<IP>', parsed_log['message'])
            # Normalize numbers
            message = re.sub(r'\b\d{4,}\b', '<NUM>', message)
            # Normalize paths
            message = re.sub(r'\/\S+', '<PATH>', message)
            parts.append(message)
        
        return " ".join(parts)
    
    def prepare_training_data(self, log_file: str) -> Tuple[List[str], List[str]]:
        """
        Prepare logs for GPT-2 training.
        Returns (processed_logs, labels)
        """
        processed_logs = []
        labels = []
        
        with open(log_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                
                # Parse and normalize
                parsed = self.parse_log(line)
                normalized = self.normalize_log(parsed)
                processed_logs.append(normalized)
                
                # Simple anomaly detection for labeled data
                # In real life, you'd have actual labels
                is_anomaly = (
                    not parsed.get("parsed") or
                    "error" in line.lower() or
                    "failed" in line.lower() or
                    "denied" in line.lower()
                )
                labels.append("anomaly" if is_anomaly else "normal")
        
        return processed_logs, labels
    
    def create_sequences(self, logs: List[str], sequence_length: int = 10) -> List[str]:
        """
        Create sequences of logs for training.
        GPT-2 learns patterns better with context.
        """
        sequences = []
        
        for i in range(len(logs) - sequence_length + 1):
            sequence = " <SEP> ".join(logs[i:i + sequence_length])
            sequences.append(sequence)
        
        return sequences

# Test the preprocessor
preprocessor = LogPreprocessor()

# Sample logs
sample_logs = [
    "2024-01-15 10:00:00 INFO User admin logged in from 192.168.1.100",
    "2024-01-15 10:00:01 ERROR Database connection failed",
    "2024-01-15 10:00:02 INFO Processing request from 192.168.1.101",
    "CRITICAL SYSTEM MELTDOWN IMMINENT!!!",  # This should be flagged
]

for log in sample_logs:
    parsed = preprocessor.parse_log(log)
    normalized = preprocessor.normalize_log(parsed)
    print(f"Original: {log}")
    print(f"Normalized: {normalized}")
    print(f"Parsed successfully: {parsed.get('parsed', False)}")
    print("-" * 50)
```

**Day 8-10: Fine-tuning GPT-2**

Now for the fun part - teaching GPT-2 about your logs:

```python
from transformers import (
    GPT2LMHeadModel, 
    GPT2Tokenizer, 
    GPT2Config,
    DataCollatorForLanguageModeling,
    Trainer, 
    TrainingArguments
)
from torch.utils.data import Dataset
import torch
import numpy as np

class LogDataset(Dataset):
    """
    Custom dataset for log sequences.
    Like a playlist, but for security events.
    """
    
    def __init__(self, sequences: List[str], tokenizer, max_length: int = 512):
        self.sequences = sequences
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.sequences)
    
    def __getitem__(self, idx):
        sequence = self.sequences[idx]
        
        # Tokenize
        encoded = self.tokenizer(
            sequence,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        # For language modeling, input_ids and labels are the same
        input_ids = encoded['input_ids'].squeeze()
        attention_mask = encoded['attention_mask'].squeeze()
        
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': input_ids  # GPT-2 predicts the next token
        }

class LogGPT2AnomalyDetector:
    """
    The main event: GPT-2 for log anomaly detection.
    It's like GPT-2, but paranoid about your logs.
    """
    
    def __init__(self, model_name: str = "gpt2", device: str = None):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load tokenizer and add special tokens
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        special_tokens = {
            'pad_token': '<PAD>',
            'sep_token': '<SEP>',
            'additional_special_tokens': [
                '<TIME>', '<IP>', '<PATH>', '<NUM>', 
                '<INFO>', '<ERROR>', '<WARNING>', '<CRITICAL>',
                '<ANOMALY>'
            ]
        }
        self.tokenizer.add_special_tokens(special_tokens)
        
        # Load model and resize embeddings
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.model.resize_token_embeddings(len(self.tokenizer))
        self.model.to(self.device)
        
        self.perplexity_threshold = None  # Set during training
        
    def train(self, train_sequences: List[str], val_sequences: List[str], 
              output_dir: str = "./log-gpt2", epochs: int = 3):
        """
        Fine-tune GPT-2 on your logs.
        Warning: May cause your GPU to question its life choices.
        """
        print(f"Training on {len(train_sequences)} sequences")
        
        # Create datasets
        train_dataset = LogDataset(train_sequences, self.tokenizer)
        val_dataset = LogDataset(val_sequences, self.tokenizer)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=4,  # Adjust based on GPU memory
            per_device_eval_batch_size=4,
            gradient_accumulation_steps=4,  # Effective batch size = 16
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir=f'{output_dir}/logs',
            logging_steps=10,
            eval_steps=500,
            save_steps=1000,
            evaluation_strategy="steps",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            fp16=self.device == 'cuda',  # Mixed precision on GPU
            push_to_hub=False,  # Unless you want to share your log model
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,  # GPT-2 is not a masked language model
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator,
            tokenizer=self.tokenizer,
        )
        
        # Train!
        print("Starting training... (This is a good time for coffee)")
        trainer.train()
        
        # Save the fine-tuned model
        trainer.save_model(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        
        # Calculate perplexity threshold on normal logs
        self._calculate_threshold(val_sequences[:100])  # Use first 100 normal logs
        
        print(f"Training complete! Model saved to {output_dir}")
        print(f"Perplexity threshold set to: {self.perplexity_threshold:.2f}")
        
    def _calculate_threshold(self, normal_sequences: List[str], percentile: int = 95):
        """
        Calculate perplexity threshold based on normal logs.
        Like setting your paranoia level.
        """
        perplexities = []
        
        for sequence in normal_sequences:
            perplexity = self.calculate_perplexity(sequence)
            perplexities.append(perplexity)
        
        # Set threshold at 95th percentile of normal logs
        self.perplexity_threshold = np.percentile(perplexities, percentile)
        
    def calculate_perplexity(self, sequence: str) -> float:
        """
        Calculate perplexity for a log sequence.
        High perplexity = "This looks weird to me"
        """
        self.model.eval()
        
        # Tokenize
        inputs = self.tokenizer(
            sequence, 
            return_tensors='pt',
            truncation=True,
            max_length=512
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            loss = outputs.loss
            perplexity = torch.exp(loss).item()
        
        return perplexity
    
    def detect_anomaly(self, log_sequence: str) -> Dict:
        """
        Detect if a log sequence is anomalous.
        Returns confidence score and reasoning.
        """
        perplexity = self.calculate_perplexity(log_sequence)
        
        if self.perplexity_threshold is None:
            raise ValueError("Model not trained! Run train() first.")
        
        is_anomaly = perplexity > self.perplexity_threshold
        confidence = min(1.0, (perplexity / self.perplexity_threshold) - 1.0) if is_anomaly else 0.0
        
        return {
            'is_anomaly': is_anomaly,
            'confidence': confidence,
            'perplexity': perplexity,
            'threshold': self.perplexity_threshold,
            'reasoning': self._generate_reasoning(log_sequence, perplexity)
        }
    
    def _generate_reasoning(self, sequence: str, perplexity: float) -> str:
        """
        Generate human-readable explanation.
        Because "computer says no" isn't helpful.
        """
        if perplexity < self.perplexity_threshold:
            return "Log sequence follows normal patterns"
        elif perplexity < self.perplexity_threshold * 1.5:
            return "Slightly unusual pattern detected - worth investigating"
        elif perplexity < self.perplexity_threshold * 2:
            return "Significant deviation from normal behavior"
        else:
            return "Highly anomalous - never seen this pattern before!"
    
    def detect_anomalies_streaming(self, log_file: str, window_size: int = 10):
        """
        Stream logs and detect anomalies in real-time.
        Like a security camera, but for text.
        """
        print(f"Starting real-time anomaly detection on {log_file}")
        print("Press Ctrl+C to stop\n")
        
        window = []
        
        try:
            with open(log_file, 'r') as f:
                # Move to end of file
                f.seek(0, 2)
                
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)  # Wait for new logs
                        continue
                    
                    # Process log
                    parsed = preprocessor.parse_log(line.strip())
                    normalized = preprocessor.normalize_log(parsed)
                    
                    # Update window
                    window.append(normalized)
                    if len(window) > window_size:
                        window.pop(0)
                    
                    # Check for anomalies
                    if len(window) == window_size:
                        sequence = " <SEP> ".join(window)
                        result = self.detect_anomaly(sequence)
                        
                        if result['is_anomaly']:
                            print(f"\n🚨 ANOMALY DETECTED! Confidence: {result['confidence']:.2%}")
                            print(f"   Perplexity: {result['perplexity']:.2f} (threshold: {result['threshold']:.2f})")
                            print(f"   Reasoning: {result['reasoning']}")
                            print(f"   Context: {line.strip()}")
                            print("-" * 80)
                    
        except KeyboardInterrupt:
            print("\nStopping anomaly detection...")

# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = LogGPT2AnomalyDetector(model_name="gpt2")
    
    # Prepare training data
    preprocessor = LogPreprocessor()
    
    # Load your logs (you'd use your actual log files here)
    train_logs, _ = preprocessor.prepare_training_data("train_logs.txt")
    val_logs, _ = preprocessor.prepare_training_data("val_logs.txt")
    
    # Create sequences
    train_sequences = preprocessor.create_sequences(train_logs)
    val_sequences = preprocessor.create_sequences(val_logs)
    
    # Train the model
    detector.train(train_sequences, val_sequences, epochs=3)
    
    # Test on some examples
    test_sequences = [
        "<TIME> <INFO> User admin logged in from <IP> <SEP> <TIME> <INFO> User admin accessed <PATH>",
        "<TIME> <ERROR> Database connection failed <SEP> <TIME> <CRITICAL> System shutdown initiated",
        "<TIME> <INFO> User root logged in from <IP> <SEP> <TIME> <INFO> User root deleted all files"
    ]
    
    for seq in test_sequences:
        result = detector.detect_anomaly(seq)
        print(f"Sequence: {seq[:50]}...")
        print(f"Anomaly: {result['is_anomaly']}, Confidence: {result['confidence']:.2%}")
        print(f"Reasoning: {result['reasoning']}")
        print("-" * 50)
```

### Phase 3: Advanced Techniques (Week 4-5)
#### *"Making It Production-Ready (Or At Least Not Embarrassing)"*

**Day 11-14: Reinforcement Learning Fine-tuning**

Remember LogGPT from the research? Let's implement their reinforcement learning approach:

```python
import torch.nn.functional as F
from torch.optim import AdamW
from collections import deque
import random

class ReinforcementLogGPT:
    """
    GPT-2 with reinforcement learning for better anomaly detection.
    It learns from its mistakes, unlike some developers I know.
    """
    
    def __init__(self, base_model_path: str, learning_rate: float = 1e-5):
        # Load the fine-tuned model
        self.tokenizer = GPT2Tokenizer.from_pretrained(base_model_path)
        self.model = GPT2LMHeadModel.from_pretrained(base_model_path)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # RL components
        self.optimizer = AdamW(self.model.parameters(), lr=learning_rate)
        self.memory = deque(maxlen=1000)  # Experience replay buffer
        self.epsilon = 0.1  # Exploration rate
        
        # Reward settings
        self.rewards = {
            'true_positive': 10.0,   # Correctly identified anomaly
            'true_negative': 1.0,    # Correctly identified normal
            'false_positive': -5.0,  # Cried wolf
            'false_negative': -10.0  # Missed an attack (worst case)
        }
        
    def remember(self, state, action, reward, next_state):
        """Store experience in replay buffer."""
        self.memory.append((state, action, reward, next_state))
    
    def act(self, sequence: str, training: bool = False) -> Dict:
        """
        Decide if sequence is anomalous.
        In training mode, sometimes explores random actions.
        """
        if training and random.random() < self.epsilon:
            # Exploration: random action
            is_anomaly = random.choice([True, False])
            confidence = random.random()
        else:
            # Exploitation: use model
            result = self.detect_anomaly(sequence)
            is_anomaly = result['is_anomaly']
            confidence = result['confidence']
        
        return {
            'is_anomaly': is_anomaly,
            'confidence': confidence,
            'sequence': sequence
        }
    
    def replay(self, batch_size: int = 32):
        """
        Train on past experiences.
        Like learning from your mistakes, but automated.
        """
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        total_loss = 0
        
        for state, action, reward, next_state in batch:
            # Calculate loss based on reward
            # Positive reward = reinforce behavior
            # Negative reward = discourage behavior
            
            inputs = self.tokenizer(
                state, 
                return_tensors='pt',
                truncation=True,
                max_length=512
            ).to(self.device)
            
            outputs = self.model(**inputs, labels=inputs['input_ids'])
            
            # Modify loss based on reward
            loss = outputs.loss * (-reward * 0.1)  # Scale reward impact
            
            # Backprop
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / batch_size
    
    def train_with_feedback(self, labeled_sequences: List[Tuple[str, bool]], epochs: int = 5):
        """
        Train with human feedback on what's actually anomalous.
        Because sometimes the model needs adult supervision.
        """
        print(f"Training with feedback on {len(labeled_sequences)} sequences")
        
        for epoch in range(epochs):
            correct = 0
            total = 0
            epoch_rewards = []
            
            # Shuffle data
            random.shuffle(labeled_sequences)
            
            for sequence, is_actually_anomaly in labeled_sequences:
                # Model prediction
                action = self.act(sequence, training=True)
                predicted_anomaly = action['is_anomaly']
                
                # Calculate reward
                if predicted_anomaly == is_actually_anomaly:
                    if is_actually_anomaly:
                        reward = self.rewards['true_positive']
                    else:
                        reward = self.rewards['true_negative']
                    correct += 1
                else:
                    if predicted_anomaly:
                        reward = self.rewards['false_positive']
                    else:
                        reward = self.rewards['false_negative']
                
                # Store experience
                self.remember(sequence, predicted_anomaly, reward, sequence)
                epoch_rewards.append(reward)
                total += 1
                
                # Learn from replay buffer
                if len(self.memory) > 32:
                    self.replay()
            
            # Decay exploration
            self.epsilon = max(0.01, self.epsilon * 0.95)
            
            # Print progress
            accuracy = correct / total
            avg_reward = sum(epoch_rewards) / len(epoch_rewards)
            print(f"Epoch {epoch + 1}/{epochs} - Accuracy: {accuracy:.2%}, Avg Reward: {avg_reward:.2f}")
    
    def adaptive_threshold_update(self, feedback_history: List[Dict]):
        """
        Dynamically adjust detection threshold based on feedback.
        Because static thresholds are so last year.
        """
        # Analyze false positive/negative rates
        false_positives = sum(1 for f in feedback_history if f['type'] == 'false_positive')
        false_negatives = sum(1 for f in feedback_history if f['type'] == 'false_negative')
        
        # Adjust threshold
        if false_positives > false_negatives * 2:
            # Too many false alarms - increase threshold
            self.perplexity_threshold *= 1.1
            print(f"Increased threshold to {self.perplexity_threshold:.2f} (too many false positives)")
        elif false_negatives > false_positives:
            # Missing too many anomalies - decrease threshold
            self.perplexity_threshold *= 0.9
            print(f"Decreased threshold to {self.perplexity_threshold:.2f} (too many false negatives)")

# Example training with feedback
rl_detector = ReinforcementLogGPT("./log-gpt2")

# Simulated labeled data (in practice, from security analyst feedback)
labeled_data = [
    # (sequence, is_anomaly)
    ("<TIME> <INFO> User admin login from <IP>", False),
    ("<TIME> <ERROR> Unauthorized access attempt blocked", True),
    ("<TIME> <INFO> Scheduled backup completed", False),
    ("<TIME> <CRITICAL> rm -rf / executed by root", True),
    # ... more labeled examples
]

# Train with reinforcement learning
rl_detector.train_with_feedback(labeled_data, epochs=10)
```

**Day 15-17: Production Deployment**

Time to make this thing actually useful in the real world:

```python
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel
import asyncio
import aiofiles
from typing import Optional
import uvicorn
from datetime import datetime
import redis
import json

# API Models
class LogEntry(BaseModel):
    timestamp: datetime
    log_line: str
    source: str
    
class AnomalyAlert(BaseModel):
    timestamp: datetime
    log_line: str
    confidence: float
    perplexity: float
    reasoning: str
    context: List[str]  # Surrounding logs

class ProductionLogAnomalyDetector:
    """
    Production-ready anomaly detection service.
    Now with 100% more enterprise features!
    """
    
    def __init__(self, model_path: str, redis_host: str = "localhost"):
        # Load model
        self.detector = LogGPT2AnomalyDetector()
        self.detector.model = GPT2LMHeadModel.from_pretrained(model_path)
        self.detector.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        
        # Redis for caching and rate limiting
        self.redis_client = redis.Redis(host=redis_host, decode_responses=True)
        
        # Performance metrics
        self.metrics = {
            'total_processed': 0,
            'anomalies_detected': 0,
            'processing_time_ms': deque(maxlen=1000),
            'false_positives': 0,
            'true_positives': 0
        }
        
        # Alert fatigue prevention
        self.alert_cooldown = 300  # 5 minutes
        self.similar_alert_threshold = 0.8  # Similarity threshold
        
    async def process_log_stream(self, log_source: str, websocket: Optional[WebSocket] = None):
        """
        Process logs in real-time with all the production goodies.
        """
        window = deque(maxlen=10)
        
        async with aiofiles.open(log_source, 'r') as f:
            while True:
                line = await f.readline()
                if not line:
                    await asyncio.sleep(0.1)
                    continue
                
                start_time = datetime.now()
                
                # Process log
                processed = self._process_log_line(line.strip())
                window.append(processed)
                
                if len(window) == 10:
                    # Check for anomalies
                    result = await self._check_anomaly_async(list(window))
                    
                    # Record metrics
                    processing_time = (datetime.now() - start_time).total_seconds() * 1000
                    self.metrics['processing_time_ms'].append(processing_time)
                    self.metrics['total_processed'] += 1
                    
                    if result['is_anomaly']:
                        # Check for alert fatigue
                        if not self._is_duplicate_alert(result):
                            alert = self._create_alert(result, list(window))
                            
                            # Send alert
                            if websocket:
                                await websocket.send_json(alert.dict())
                            
                            # Store in Redis
                            self._store_alert(alert)
                            
                            self.metrics['anomalies_detected'] += 1
    
    async def _check_anomaly_async(self, window: List[str]) -> Dict:
        """Async anomaly detection to not block the stream."""
        # Run CPU-intensive work in thread pool
        loop = asyncio.get_event_loop()
        sequence = " <SEP> ".join(window)
        result = await loop.run_in_executor(None, self.detector.detect_anomaly, sequence)
        return result
    
    def _is_duplicate_alert(self, result: Dict) -> bool:
        """
        Check if we've seen a similar alert recently.
        Prevents alert fatigue from repeated similar anomalies.
        """
        recent_alerts = self.redis_client.zrange(
            'recent_alerts', 
            0, 
            -1, 
            withscores=True
        )
        
        current_time = datetime.now().timestamp()
        
        for alert_json, timestamp in recent_alerts:
            # Skip old alerts
            if current_time - timestamp > self.alert_cooldown:
                continue
            
            alert = json.loads(alert_json)
            
            # Simple similarity check (you could use more sophisticated methods)
            if abs(alert['perplexity'] - result['perplexity']) < 10:
                return True
        
        return False
    
    def _store_alert(self, alert: AnomalyAlert):
        """Store alert in Redis with expiration."""
        alert_json = json.dumps(alert.dict(), default=str)
        timestamp = datetime.now().timestamp()
        
        # Store with timestamp score for ordering
        self.redis_client.zadd('recent_alerts', {alert_json: timestamp})
        
        # Expire old entries
        self.redis_client.zremrangebyscore(
            'recent_alerts', 
            0, 
            timestamp - self.alert_cooldown
        )
    
    def _create_alert(self, result: Dict, context: List[str]) -> AnomalyAlert:
        """Create a structured alert."""
        return AnomalyAlert(
            timestamp=datetime.now(),
            log_line=context[-1],  # Most recent log
            confidence=result['confidence'],
            perplexity=result['perplexity'],
            reasoning=result['reasoning'],
            context=context
        )
    
    def get_metrics(self) -> Dict:
        """Get performance metrics."""
        avg_processing_time = (
            sum(self.metrics['processing_time_ms']) / len(self.metrics['processing_time_ms'])
            if self.metrics['processing_time_ms'] else 0
        )
        
        detection_rate = (
            self.metrics['anomalies_detected'] / self.metrics['total_processed']
            if self.metrics['total_processed'] > 0 else 0
        )
        
        return {
            'total_processed': self.metrics['total_processed'],
            'anomalies_detected': self.metrics['anomalies_detected'],
            'avg_processing_time_ms': avg_processing_time,
            'detection_rate': detection_rate,
            'logs_per_second': 1000 / avg_processing_time if avg_processing_time > 0 else 0
        }

# FastAPI Application
app = FastAPI(title="LogGPT Anomaly Detection API")

# Global detector instance
detector = None

@app.on_event("startup")
async def startup_event():
    global detector
    detector = ProductionLogAnomalyDetector("./log-gpt2")
    print("LogGPT Anomaly Detector initialized!")

@app.post("/analyze")
async def analyze_logs(entry: LogEntry):
    """Analyze a single log entry."""
    # Process and analyze
    result = detector.detector.detect_anomaly(entry.log_line)
    
    return {
        "timestamp": entry.timestamp,
        "is_anomaly": result['is_anomaly'],
        "confidence": result['confidence'],
        "reasoning": result['reasoning']
    }

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    """Real-time log streaming and anomaly detection."""
    await websocket.accept()
    
    try:
        # Start processing logs
        await detector.process_log_stream("/var/log/app.log", websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/metrics")
async def get_metrics():
    """Get performance metrics."""
    return detector.get_metrics()

@app.post("/feedback")
async def submit_feedback(
    log_line: str, 
    was_correct: bool, 
    actual_label: bool
):
    """Submit feedback for continuous improvement."""
    feedback_type = "true_positive" if was_correct else "false_positive"
    
    # Store feedback for retraining
    detector.redis_client.lpush(
        'feedback_queue',
        json.dumps({
            'log_line': log_line,
            'actual_label': actual_label,
            'feedback_type': feedback_type,
            'timestamp': datetime.now().isoformat()
        })
    )
    
    return {"status": "Feedback recorded"}

# Run the API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Phase 4: Advanced Features and Optimization (Week 6)
#### *"Making It Scary Good"*

**Day 18-20: Multi-Model Ensemble**

Because one paranoid AI isn't enough:

```python
class EnsembleAnomalyDetector:
    """
    Multiple models voting on anomalies.
    Democracy, but for AI paranoia.
    """
    
    def __init__(self, model_configs: List[Dict]):
        self.models = []
        
        for config in model_configs:
            if config['type'] == 'gpt2':
                model = LogGPT2AnomalyDetector(config['path'])
            elif config['type'] == 'statistical':
                model = StatisticalAnomalyDetector(config['params'])
            elif config['type'] == 'isolation_forest':
                model = IsolationForestDetector(config['params'])
            
            self.models.append({
                'model': model,
                'weight': config.get('weight', 1.0),
                'name': config['name']
            })
    
    def detect_anomaly(self, log_sequence: str) -> Dict:
        """
        Get consensus from all models.
        Like a security council, but faster.
        """
        votes = []
        details = []
        
        for model_info in self.models:
            model = model_info['model']
            weight = model_info['weight']
            name = model_info['name']
            
            result = model.detect_anomaly(log_sequence)
            
            # Weighted voting
            vote = result['confidence'] * weight if result['is_anomaly'] else 0
            votes.append(vote)
            
            details.append({
                'model': name,
                'vote': vote,
                'reasoning': result.get('reasoning', 'No explanation')
            })
        
        # Calculate consensus
        avg_vote = sum(votes) / len(votes)
        is_anomaly = avg_vote > 0.5
        
        return {
            'is_anomaly': is_anomaly,
            'confidence': avg_vote,
            'model_votes': details,
            'consensus': self._get_consensus_explanation(details, avg_vote)
        }
    
    def _get_consensus_explanation(self, details: List[Dict], avg_vote: float) -> str:
        """Generate human-readable consensus explanation."""
        if avg_vote > 0.8:
            return "Strong consensus: Highly anomalous activity detected"
        elif avg_vote > 0.6:
            return "Moderate consensus: Suspicious activity detected"
        elif avg_vote > 0.4:
            return "Weak consensus: Potentially unusual activity"
        else:
            return "No consensus: Activity appears normal"

# Configuration for ensemble
ensemble_config = [
    {
        'name': 'GPT2-Base',
        'type': 'gpt2',
        'path': './log-gpt2',
        'weight': 2.0  # Trust GPT-2 more
    },
    {
        'name': 'Statistical',
        'type': 'statistical',
        'params': {'threshold': 3.0},
        'weight': 1.0
    },
    {
        'name': 'IsolationForest',
        'type': 'isolation_forest',
        'params': {'contamination': 0.01},
        'weight': 1.5
    }
]

# Create ensemble
ensemble = EnsembleAnomalyDetector(ensemble_config)
```

**Day 21: Performance Optimization**

Making it fast enough for production:

```python
import onnxruntime as ort
from transformers import GPT2Tokenizer
import numpy as np

class OptimizedLogGPT:
    """
    ONNX-optimized GPT-2 for blazing fast inference.
    Because nobody has time for slow anomaly detection.
    """
    
    def __init__(self, model_path: str, onnx_path: str = None):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        
        if onnx_path is None:
            # Convert to ONNX
            self._convert_to_onnx(model_path)
            onnx_path = f"{model_path}/model.onnx"
        
        # Load ONNX model
        self.session = ort.InferenceSession(onnx_path)
        
        # Batch processing queue
        self.batch_queue = []
        self.batch_size = 16
        
    def _convert_to_onnx(self, model_path: str):
        """Convert PyTorch model to ONNX for faster inference."""
        from transformers import GPT2LMHeadModel
        import torch
        
        model = GPT2LMHeadModel.from_pretrained(model_path)
        model.eval()
        
        # Dummy input
        dummy_input = torch.randint(0, 50000, (1, 512))
        
        # Export
        torch.onnx.export(
            model,
            dummy_input,
            f"{model_path}/model.onnx",
            input_names=['input_ids'],
            output_names=['logits'],
            dynamic_axes={
                'input_ids': {0: 'batch_size', 1: 'sequence'},
                'logits': {0: 'batch_size', 1: 'sequence'}
            },
            opset_version=11
        )
        
        print(f"Model converted to ONNX: {model_path}/model.onnx")
    
    def batch_detect_anomalies(self, sequences: List[str]) -> List[Dict]:
        """
        Process multiple sequences in batch for efficiency.
        Like carpooling, but for AI inference.
        """
        # Tokenize all sequences
        encoded = self.tokenizer(
            sequences,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='np'
        )
        
        # Run inference
        input_ids = encoded['input_ids'].astype(np.int64)
        
        outputs = self.session.run(
            None,
            {'input_ids': input_ids}
        )
        
        logits = outputs[0]
        
        # Calculate perplexities
        results = []
        for i, sequence in enumerate(sequences):
            # Simplified perplexity calculation
            log_probs = self._calculate_log_probs(logits[i])
            perplexity = np.exp(-np.mean(log_probs))
            
            results.append({
                'sequence': sequence,
                'perplexity': perplexity,
                'is_anomaly': perplexity > self.threshold
            })
        
        return results

# Usage
optimized_detector = OptimizedLogGPT("./log-gpt2")

# Batch processing
sequences = [
    "Normal log sequence 1",
    "Normal log sequence 2", 
    "Suspicious activity detected",
    # ... more sequences
]

results = optimized_detector.batch_detect_anomalies(sequences)
print(f"Processed {len(results)} sequences in batch")
```

## Real-World Applications
### *"Where This Actually Gets Used (Besides Your Resume)"*

1. **Security Operations Centers (SOCs)**
   - Real-time threat detection
   - Reduced false positives
   - Automated tier-1 analysis

2. **Cloud Infrastructure Monitoring**
   - Detect configuration drift
   - Spot resource abuse
   - Identify service degradation

3. **Compliance and Auditing**
   - Automated log review
   - Anomaly reporting
   - Pattern identification

4. **DevOps and SRE**
   - Faster incident detection
   - Root cause analysis
   - Predictive failure detection

## Common Pitfalls and How to Avoid Them
### *"Learn From My Mistakes So You Don't Have To"*

1. **The "It Worked in Dev" Syndrome**
   - Test with real production log volumes
   - Monitor resource usage
   - Have fallback mechanisms

2. **The "Everything Is An Anomaly" Problem**
   - Proper threshold tuning
   - Continuous feedback loop
   - Context-aware detection

3. **The "Model Drift" Disaster**
   - Regular retraining
   - Monitor model performance
   - Version control your models

4. **The "Privacy Oops" Moment**
   - Anonymize sensitive data
   - Don't train on PII
   - Implement data retention policies

## Next Steps and Advanced Topics
### *"Because There's Always More to Learn"*

1. **Advanced Model Architectures**
   - Try GPT-3 or LLaMA for better context understanding
   - Experiment with specialized security models
   - Multi-modal detection (logs + metrics)

2. **Integration Projects**
   - Build a Splunk plugin
   - Create a Kubernetes operator
   - Integrate with SIEM systems

3. **Research Frontiers**
   - Few-shot learning for new log types
   - Cross-system anomaly correlation
   - Adversarial robustness

## Resources and References
### *"Standing on the Shoulders of Giants"*

- **Papers**:
  - "LogGPT: Log Anomaly Detection via GPT" (arXiv:2309.14482)
  - "Anomaly Detection on Unstable Logs with GPT Models" (arXiv:2406.07467)

- **Code Repositories**:
  - [Hugging Face Transformers](https://github.com/huggingface/transformers)
  - [LogAnomalyDetection Benchmarks](https://github.com/logpai/loglizer)

- **Datasets**:
  - [Loghub](https://github.com/logpai/loghub) - Collection of system log datasets
  - [HDFS Log Dataset](https://github.com/logpai/loghub/tree/master/HDFS)

## Final Thoughts
### *"You Made It! Now What?"*

Congratulations! You've just built an AI-powered log anomaly detection system that would make any SOC analyst jealous. You've learned:

- How to fine-tune GPT-2 for domain-specific tasks
- Real-time log processing at scale
- Production deployment with actual error handling
- Why sleep is overrated when you have anomalies to detect

Remember: The best anomaly detector is the one that's actually running in production, not the perfect one sitting in a Jupyter notebook.

Now go forth and detect those anomalies! And when you catch your first real attack at 3 AM, remember to thank GPT-2 (and maybe get some sleep).

---

*"In the world of log analysis, paranoia is just another word for experience."* - Every Security Engineer Ever