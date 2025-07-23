import numpy as np

class KalmanFilter:
    def __init__(self):
        ndim, dt = 4, 1.
        self._motion_mat = np.eye(2 * ndim)
        for i in range(ndim):
            self._motion_mat[i, ndim + i] = dt
        self._update_mat = np.eye(ndim, 2 * ndim)

        self._std_weight_position = 1. / 20
        self._std_weight_velocity = 1. / 160

    def initiate(self, measurement):
        mean_pos = measurement
        mean_vel = np.zeros_like(mean_pos)
        mean = np.r_[mean_pos, mean_vel]

        std = [2 * self._std_weight_position * measurement[3]] * 4 + \
              [10 * self._std_weight_velocity * measurement[3]] * 4
        covariance = np.diag(np.square(std))
        return mean, covariance

    def predict(self, mean, covariance):
        std_pos = [self._std_weight_position * mean[3]] * 4
        std_vel = [self._std_weight_velocity * mean[3]] * 4
        motion_cov = np.diag(np.square(std_pos + std_vel))

        mean = np.dot(self._motion_mat, mean)
        covariance = np.dot(np.dot(self._motion_mat, covariance), self._motion_mat.T) + motion_cov
        return mean, covariance

    def update(self, mean, covariance, measurement):
        std = [self._std_weight_position * mean[3]] * 4
        innovation_cov = np.diag(np.square(std))

        projected_mean = np.dot(self._update_mat, mean)
        projected_cov = np.dot(np.dot(self._update_mat, covariance), self._update_mat.T) + innovation_cov

        kalman_gain = np.dot(np.dot(covariance, self._update_mat.T), np.linalg.inv(projected_cov))
        innovation = measurement - projected_mean

        new_mean = mean + np.dot(kalman_gain, innovation)
        new_covariance = covariance - np.dot(np.dot(kalman_gain, self._update_mat), covariance)
        return new_mean, new_covariance