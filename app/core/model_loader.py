import onnxruntime as ort
from app.config import MODEL_PATH, MODEL_INPUT_SIZE, NUM_THREADS

class ModelLoader:
    _instance = None
    
    def __init__(self):
        if ModelLoader._instance is not None:
            raise Exception("ModelLoader is a singleton! Use get_instance()")
        
        sess_opts = ort.SessionOptions()
        sess_opts.intra_op_num_threads = NUM_THREADS
        sess_opts.execution_mode = ort.ExecutionMode.ORT_PARALLEL
        sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.session = ort.InferenceSession(
            MODEL_PATH,
            sess_options=sess_opts,
            providers=["CPUExecutionProvider"]
        )
        self.input_name = self.session.get_inputs()[0].name
        ModelLoader._instance = self
    
    @staticmethod
    def get_instance():
        if ModelLoader._instance is None:
            ModelLoader()
        return ModelLoader._instance