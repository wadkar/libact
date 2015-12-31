"""
Base interfaces for use in the package.
The package works according to the interfaces defined below.
"""

from abc import ABCMeta, abstractmethod


class QueryStrategy(metaclass=ABCMeta):
    """Pool-based query strategy

    A QueryStrategy advices on which unlabeled data to be queried next given 
    a pool of labeled and unlabeled data.
    """
    def __init__(self, dataset, **kwargs):
        self._dataset = dataset
        dataset.on_update(self.update)

    @property
    def dataset(self):
        return self._dataset

    def update(self, entry_id, label):
        """Update the internal states of the QueryStrategy after each queried 
        sample being labeled.

        Parameters
        ----------
        entry_id : float
            The index of the newly labeled sample.
            
        label : float
            The label of the queried sample.
        
        Returns
        -------
        self : object
            Returns self.
        """
        pass

    @abstractmethod
    def make_query(self):
        """Return the index of the sample to be queried and labeled. Read-only.
        
        No modification to the internal states.
        
        Returns
        -------
        ask_id : float
            The index of the next unlabeled sample to be queried and labeled.
        """
        pass


class Labeler(metaclass=ABCMeta):
    """Label the queries made by QueryStrategies
    
    Assign labels to the samples queried by QueryStrategies.
    """
    @abstractmethod
    def label(self, feature):
        """Return the class labels for the input feature array. 
    
        Parameters
        ----------
        feautre : array, shape (n_features,)
            The feature vector whose label is to queried.
            
        Returns
        -------
        label : float
            The class label of the queried feature.
        """        
        pass


class Model(metaclass=ABCMeta):
    """Classification Model

    A Model retruns a class-predicting function for future samples after 
    trained on a training dataset.
    """
    @abstractmethod
    def train(self, dataset, *args, **kwargs):
        """Train a model according to the given training dataset. 
        
        Parameters
        ----------
        dataset : Dataset object
             The training dataset the model is to be trained on.

        Returns
        -------
        self : object
            Returns self.
        """        
        pass

    @abstractmethod
    def predict(self, feature, *args, **kwargs):
        """Predict the class labels for the input samples
        
        Parameters
        ----------
        feature : array, shape (n_samples, n_features)
            The unlabeled samples whose labels are to be predicted.
            
        Returns
        -------
        y_pred : array, shape (n_samples,)
            The class labels for samples in the feature array.
        """
        pass

    @abstractmethod
    def score(self, testing_dataset, *args, **kwargs):
        """Return the mean accuracy on the test dataset
        
        Parameters
        ----------
        testing_dataset : Dataset object
            The testing dataset used to measure the perforance of the trained model.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        pass


class ContinuousModel(Model):
    """Classification Model with intermediate continuous output
    
    A continuous classification model is able to output a real-valued vector
    for each features provided.
    """
    @abstractmethod
    def predict_real(self, feature, *args, **kwargs):
        """Predict confidence scores for samples. 
        
        This method returns the confidence score of each class for each sample.
        The larger this value is, the more confident this model is sure about
        whether this sample belongs to this class or not.
        Take Logistic Regression as example, the return value is the is the
        signed distance of that sample to the hyperplane.
        
        Parameters
        ----------
        feature : array, shape (n_samples, n_features)
            The samples whose confidence scores are to be predicted.

        Returns
        -------
        X : array-like, shape (n_samples, n_classes)
            Each entry is the confidence scores per (sample, class) combination.        
        """
        pass
