import { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, FileText, Image as ImageIcon } from 'lucide-react';
import { InputMode, CodeInput } from '../types';

interface InputZoneProps {
  onVisualize: (input: string, mode: InputMode, codeInput?: CodeInput) => void;
  onUploadImage?: (file: File) => Promise<void>;
  isProcessing: boolean;
}

export function InputZone({ onVisualize, onUploadImage, isProcessing }: InputZoneProps) {
  const [mode, setMode] = useState<'text' | 'image'>('text');
  const [textInput, setTextInput] = useState('');
  const [fileName, setFileName] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);

  const handleVisualize = () => {
    if (mode === 'text' && textInput.trim()) {
      onVisualize(textInput, mode);
    } else if (mode === 'image' && imageFile && onUploadImage) {
      onUploadImage(imageFile);
    }
  };

  const handleImageUpload = () => {
    imageInputRef.current?.click();
  };

  const onImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImageFile(file);
      setFileName(file.name);
    }
  };

  return (
    <motion.div
      initial={{ y: 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-2xl p-8"
    >
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-white mb-2">Input Zone</h2>
        <p className="text-sm text-slate-400">Describe the algorithm or upload an image to visualize</p>
      </div>

      <div className="flex gap-3 mb-6">
        <button
          onClick={() => setMode('text')}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${
            mode === 'text'
              ? 'bg-blue-500 text-white'
              : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
          }`}
        >
          <FileText className="w-5 h-5" />
          <span>Natural Language</span>
        </button>
        <button
          onClick={() => setMode('image')}
          className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all ${
            mode === 'image'
              ? 'bg-blue-500 text-white'
              : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
          }`}
        >
          <ImageIcon className="w-5 h-5" />
          <span>Whiteboard Image</span>
        </button>
      </div>

      <div className="mb-6">
        {mode === 'text' && (
          <textarea
            value={textInput}
            onChange={(e) => setTextInput(e.target.value)}
            placeholder="Describe the algorithm or data structure you want to visualize... (e.g., 'Bubble Sort algorithm visualization' or 'Explain how Binary Search works')"
            className="w-full h-48 bg-slate-950 border border-slate-700 rounded-xl p-5 text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-none text-lg"
          />
        )}

        {mode === 'image' && (
          <div 
            onClick={handleImageUpload}
            className="border-2 border-dashed border-slate-700 rounded-xl p-16 text-center cursor-pointer hover:border-blue-500 hover:bg-slate-800/50 transition-all"
          >
            {imageFile ? (
              <>
                <ImageIcon className="w-16 h-16 text-green-500 mx-auto mb-4" />
                <p className="text-green-300 text-lg mb-2">
                  {fileName}
                </p>
                <p className="text-sm text-slate-500">Click to change image</p>
              </>
            ) : (
              <>
                <ImageIcon className="w-16 h-16 text-slate-500 mx-auto mb-4" />
                <p className="text-slate-300 text-lg mb-2">
                  Click to upload a whiteboard image
                </p>
                <p className="text-sm text-slate-500">Supports .jpg, .jpeg, .png files</p>
              </>
            )}
            <input
              ref={imageInputRef}
              type="file"
              accept="image/jpeg,image/jpg,image/png"
              onChange={onImageChange}
              className="hidden"
            />
          </div>
        )}
      </div>

      <button
        onClick={handleVisualize}
        disabled={isProcessing || (!textInput.trim() && !imageFile)}
        className="w-full bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-semibold py-4 px-6 rounded-xl flex items-center justify-center gap-3 transition-all text-lg"
      >
        <Sparkles className="w-6 h-6" />
        <span>{isProcessing ? 'Processing...' : 'Visualize'}</span>
      </button>
    </motion.div>
  );
}
