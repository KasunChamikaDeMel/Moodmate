from datetime import datetime
from collections import deque
import threading
import time

class EmotionFusion:
    """Intelligent emotion fusion from multiple modalities"""
    
    WEIGHTS = {
        'face': 0.45,
        'voice': 0.40,
        'text': 0.15
    }
    
    def __init__(self, temporal_window=5):
        self.temporal_window = temporal_window
        self.recent_emotions = {
            'face': deque(maxlen=temporal_window),
            'voice': deque(maxlen=temporal_window),
            'text': deque(maxlen=temporal_window)
        }
        self.last_fused_emotion = "neutral"
        self.emotion_scores = {}
        self.lock = threading.Lock()
    
    def normalize_emotion(self, emotion):
        """
        Normalize emotion name variations to ONLY the 4 target emotions:
        Neutral, Stress, Sleep, Anger
        """
        emotion = emotion.lower().strip()
        
        # 1. Direct mappings for your target emotions
        if emotion in ['stress', 'stressed', 'fear']:
            return 'stress'
        if emotion in ['angry', 'anger']:
            return 'angry'
        if emotion in ['sleep', 'sleepy', 'sleeping', 'tired']:
            return 'sleep'
        
        # 2. Map ALL other emotions to Neutral
        return 'neutral'
    
    def add_emotion(self, modality, emotion, confidence=1.0):
        """Add emotion detection from a modality"""
        with self.lock:
            emotion = self.normalize_emotion(emotion)
            self.recent_emotions[modality].append({
                'emotion': emotion,
                'confidence': confidence,
                'timestamp': datetime.now()
            })
            print(f"📊 Added {modality}: {emotion}")
    
    def get_fused_emotion(self):
        """Compute fused emotion from all modalities"""
        with self.lock:
            emotion_scores = {}
            total_weight = 0
            
            for modality, weight in self.WEIGHTS.items():
                if not self.recent_emotions[modality]:
                    continue
                
                recent = self.recent_emotions[modality][-1]
                emotion = recent['emotion']
                confidence = recent['confidence']
                score = weight * confidence
                
                if emotion in emotion_scores:
                    emotion_scores[emotion] += score
                else:
                    emotion_scores[emotion] = score
                
                total_weight += weight
            
            if not emotion_scores:
                return "neutral", 1.0
            
            if total_weight > 0:
                emotion_scores = {e: s/total_weight for e, s in emotion_scores.items()}
            
            temporal_scores = self.calculate_temporal_scores()
            final_scores = {}
            for emotion in set(list(emotion_scores.keys()) + list(temporal_scores.keys())):
                current = emotion_scores.get(emotion, 0)
                temporal = temporal_scores.get(emotion, 0)
                final_scores[emotion] = 0.7 * current + 0.3 * temporal
            
            if final_scores:
                top_emotion = max(final_scores.items(), key=lambda x: x[1])
                fused_emotion = top_emotion[0]
                confidence = top_emotion[1]
                self.last_fused_emotion = fused_emotion
                self.emotion_scores = final_scores
                return fused_emotion, confidence
            
            return self.last_fused_emotion, 1.0
    
    def calculate_temporal_scores(self):
        """Calculate emotion scores based on recent history"""
        temporal_scores = {}
        
        for modality, weight in self.WEIGHTS.items():
            emotions = self.recent_emotions[modality]
            if not emotions:
                continue
            
            for i, item in enumerate(emotions):
                emotion = item['emotion']
                confidence = item['confidence']
                decay = 0.5 + (0.5 * (i / len(emotions)))
                score = weight * confidence * decay
                
                if emotion in temporal_scores:
                    temporal_scores[emotion] += score
                else:
                    temporal_scores[emotion] = score
        
        total = sum(temporal_scores.values())
        if total > 0:
            temporal_scores = {e: s/total for e, s in temporal_scores.items()}
        
        return temporal_scores
    
    def get_detailed_analysis(self):
        """Get detailed breakdown of current emotion state"""
        with self.lock:
            fused_emotion, confidence = self.get_fused_emotion()
            
            modality_states = {}
            for modality in ['face', 'voice', 'text']:
                if self.recent_emotions[modality]:
                    recent = self.recent_emotions[modality][-1]
                    modality_states[modality] = {
                        'emotion': recent['emotion'],
                        'confidence': recent['confidence'],
                        'weight': self.WEIGHTS[modality]
                    }
                else:
                    modality_states[modality] = None
            
            return {
                'fused_emotion': fused_emotion,
                'confidence': confidence,
                'emotion_scores': self.emotion_scores,
                'modality_states': modality_states,
                'timestamp': datetime.now().isoformat()
            }
    
    def clear_modality(self, modality):
        """Clear history for a specific modality"""
        with self.lock:
            self.recent_emotions[modality].clear()
    
    def reset(self):
        """Reset all emotion history"""
        with self.lock:
            for modality in self.recent_emotions:
                self.recent_emotions[modality].clear()
            self.last_fused_emotion = "neutral"
            self.emotion_scores = {}
            print("🔄 Emotion fusion system reset")


class ContinuousFusion:
    """Continuous emotion fusion for real-time detection"""
    
    def __init__(self, callback=None, fusion_interval=2.0):
        self.fusion = EmotionFusion(temporal_window=5)
        self.callback = callback
        self.fusion_interval = fusion_interval
        self.is_running = False
        self.thread = None
        self.last_emotion = "neutral"
    
    def start(self):
        """Start continuous fusion thread"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._fusion_loop, daemon=True)
        self.thread.start()
        print("🚀 Continuous emotion fusion started")
    
    def stop(self):
        """Stop continuous fusion thread"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("⏹️ Continuous emotion fusion stopped")
    
    def _fusion_loop(self):
        """Main fusion loop - NO CONFIDENCE CHECKS"""
        
        while self.is_running:
            fused_emotion, confidence = self.fusion.get_fused_emotion()
            
            # Only trigger callback when emotion CHANGES
            if fused_emotion != self.last_emotion:
                self.last_emotion = fused_emotion
                
                if self.callback:
                    analysis = self.fusion.get_detailed_analysis()
                    self.callback(fused_emotion, confidence, analysis)
                
                print(f"🎯 Fused Emotion: {fused_emotion}")
            
            time.sleep(self.fusion_interval)
    
    def add_face_emotion(self, emotion, confidence=1.0):
        """Add face emotion detection"""
        self.fusion.add_emotion('face', emotion, confidence)

    def add_voice_emotion(self, emotion, confidence=1.0):
        """Add voice emotion detection"""
        self.fusion.add_emotion('voice', emotion, confidence)

    def add_text_emotion(self, emotion, confidence=1.0):
        """Add text emotion detection"""
        self.fusion.add_emotion('text', emotion, confidence)
