# global
import time

import ivy
import pytest
import numpy as np
import ivy_tests.helpers as helpers

# local
from ivy_builder.dataset import MapDataset

# ToDo: find way to get multiprocessing working properly for jax and mxnet


class TestQueries:

    def _init(self, array_shape, num_processes):
        x = [ivy.array(0), ivy.array(1), ivy.array(2),
             ivy.array(3), ivy.array(4), ivy.array(5),
             ivy.array(6), ivy.array(7), ivy.array(8)]
        self._x = [ivy.reshape(item, array_shape) for item in x]
        dataset_container = ivy.Container({'x': self._x})
        self._dataset = MapDataset(dataset_container, 'base', dataset_container.shape[0], num_processes=num_processes)

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert list(self._dataset[0].x.shape) == array_shape
        assert list(self._dataset[4].x.shape) == array_shape
        assert list(self._dataset[8].x.shape) == array_shape

        assert np.allclose(ivy.to_numpy(self._dataset[0].x), ivy.to_numpy(self._x[0]))
        assert np.allclose(ivy.to_numpy(self._dataset[4].x), ivy.to_numpy(self._x[4]))
        assert np.allclose(ivy.to_numpy(self._dataset[8].x), ivy.to_numpy(self._x[8]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert list(self._dataset[9].x.shape) == array_shape
        assert list(self._dataset[11].x.shape) == array_shape
        assert list(self._dataset[-1].x.shape) == array_shape
        assert list(self._dataset[-2].x.shape) == array_shape

        assert np.allclose(ivy.to_numpy(self._dataset[9].x), ivy.to_numpy(self._x[0]))
        assert np.allclose(ivy.to_numpy(self._dataset[11].x), ivy.to_numpy(self._x[2]))
        assert np.allclose(ivy.to_numpy(self._dataset[-1].x), ivy.to_numpy(self._x[-1]))
        assert np.allclose(ivy.to_numpy(self._dataset[-2].x), ivy.to_numpy(self._x[-2]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert len(self._dataset[0:3].x) == 3
        assert list(self._dataset[0:3].x[0].shape) == array_shape
        assert len(self._dataset[3:6].x) == 3
        assert list(self._dataset[3:6].x[0].shape) == array_shape
        assert len(self._dataset[6:9].x) == 3
        assert list(self._dataset[6:9].x[0].shape) == array_shape

        assert np.allclose(ivy.to_numpy(self._dataset[0:3].x[0]), ivy.to_numpy(self._x[0]))
        assert np.allclose(ivy.to_numpy(self._dataset[3:6].x[1]), ivy.to_numpy(self._x[4]))
        assert np.allclose(ivy.to_numpy(self._dataset[6:9].x[2]), ivy.to_numpy(self._x[8]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert len(self._dataset[-1:1].x) == 2
        assert list(self._dataset[-1:1].x[0].shape) == array_shape
        assert len(self._dataset[-1:1].x) == 2
        assert list(self._dataset[-1:1].x[1].shape) == array_shape
        assert len(self._dataset[9:11].x) == 2
        assert list(self._dataset[9:11].x[0].shape) == array_shape
        assert len(self._dataset[9:11].x) == 2
        assert list(self._dataset[9:11].x[0].shape) == array_shape

        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[0]), ivy.to_numpy(self._x[8]))
        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[1]), ivy.to_numpy(self._x[0]))
        assert np.allclose(ivy.to_numpy(self._dataset[9:11].x[0]), ivy.to_numpy(self._x[0]))
        assert np.allclose(ivy.to_numpy(self._dataset[9:11].x[1]), ivy.to_numpy(self._x[1]))

        # close
        self._dataset.close()
        del self._dataset


class TestBatch:

    def _init(self, array_shape, num_processes):
        x = [ivy.array(0), ivy.array(1), ivy.array(2), ivy.array(3), ivy.array(4),
             ivy.array(5), ivy.array(6), ivy.array(7), ivy.array(8), ivy.array(9)]
        self._x = [ivy.reshape(item, array_shape) for item in x]
        dataset_container = ivy.Container({'x': self._x})
        dataset = MapDataset(dataset_container, 'base', dataset_container.shape[0], num_processes=num_processes)
        self._dataset = dataset.batch('batched', 3, num_processes=num_processes)

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0].x), np.array([[0], [1], [2]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[1].x), np.array([[3], [4], [5]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[2].x), np.array([[6], [7], [8]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[1/3].x), np.array([[1], [2], [3]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[2/3].x), np.array([[2], [3], [4]]).reshape([3] + array_shape))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[3].x), np.array([[9], [0], [1]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[4].x), np.array([[2], [3], [4]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-1].x), np.array([[7], [8], [9]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-2].x), np.array([[4], [5], [6]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-1/3].x), np.array([[9], [0], [1]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-2/3].x), np.array([[8], [9], [0]]).reshape([3] + array_shape))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[0]), np.array([[0], [1], [2]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[1]), np.array([[3], [4], [5]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[2:3].x[0]), np.array([[6], [7], [8]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[1/3:4/3].x[0]),
                           np.array([[1], [2], [3]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[2/3:5/3].x[0]),
                           np.array([[2], [3], [4]]).reshape([3] + array_shape))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[-1:0].x[0]), np.array([[7], [8], [9]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[0]), np.array([[7], [8], [9]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[1]), np.array([[0], [1], [2]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[3:4].x[0]), np.array([[9], [0], [1]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[-4/3:-1/3].x[0]),
                           np.array([[6], [7], [8]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[10/3:13/3].x[0]),
                           np.array([[0], [1], [2]]).reshape([3] + array_shape))
        assert np.allclose(ivy.to_numpy(self._dataset[8/3:11/3].x[0]),
                           np.array([[8], [9], [0]]).reshape([3] + array_shape))

        # close
        self._dataset.close()
        del self._dataset


class TestUnbatch:

    def _init(self, array_shape, num_processes):
        x = [ivy.array([[0], [1], [2]]), ivy.array([[3], [4], [5]]), ivy.array([[6], [7], [8]])]
        self._x = [ivy.reshape(item, array_shape) for item in x]
        dataset_container = ivy.Container({'x': x})
        dataset = MapDataset(dataset_container, 'base', dataset_container.shape[0], num_processes=num_processes)
        self._dataset = dataset.unbatch('unbatched', num_processes=num_processes)

    @pytest.mark.parametrize(
        "array_shape", [[3, 1], [3]])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0].x), ivy.to_numpy(self._x[0][0]))
        assert np.allclose(ivy.to_numpy(self._dataset[1].x), ivy.to_numpy(self._x[0][1]))
        assert np.allclose(ivy.to_numpy(self._dataset[2].x), ivy.to_numpy(self._x[0][2]))
        assert np.allclose(ivy.to_numpy(self._dataset[8].x), ivy.to_numpy(self._x[2][2]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[3, 1], [3]])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[9].x), ivy.to_numpy(self._x[0][0]))
        assert np.allclose(ivy.to_numpy(self._dataset[-1].x), ivy.to_numpy(self._x[2][2]))
        assert np.allclose(ivy.to_numpy(self._dataset[-2].x), ivy.to_numpy(self._x[2][1]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[3, 1], [3]])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[0]), ivy.to_numpy(self._x[0][0]))
        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[1]), ivy.to_numpy(self._x[0][1]))
        assert np.allclose(ivy.to_numpy(self._dataset[6:8].x[0]), ivy.to_numpy(self._x[2][0]))
        assert np.allclose(ivy.to_numpy(self._dataset[6:8].x[1]), ivy.to_numpy(self._x[2][1]))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[3, 1], [3]])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(array_shape, num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[0]), ivy.to_numpy(self._x[2][2]))
        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[1]), ivy.to_numpy(self._x[0][0]))
        assert np.allclose(ivy.to_numpy(self._dataset[8:10].x[0]), ivy.to_numpy(self._x[2][2]))
        assert np.allclose(ivy.to_numpy(self._dataset[8:10].x[1]), ivy.to_numpy(self._x[0][0]))

        # close
        self._dataset.close()
        del self._dataset


class TestUnbatchAndBatch:

    def _init(self, num_processes):
        self._x = [ivy.array([0, 1]),
                   ivy.array([2, 3, 4, 5, 6, 7, 8, 9])]
        dataset_container = ivy.Container({'x': self._x})
        dataset = MapDataset(dataset_container, 'base', dataset_container.shape[0], num_processes=num_processes)
        dataset = dataset.unbatch('unbatched', num_processes=num_processes)
        self._dataset = dataset.batch('batched', 3, num_processes=num_processes)

    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single(self, dev_str, f, call, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0].x), ivy.to_numpy(ivy.array([0, 1, 2])))
        assert np.allclose(ivy.to_numpy(self._dataset[1].x), ivy.to_numpy(ivy.array([3, 4, 5])))
        assert np.allclose(ivy.to_numpy(self._dataset[2].x), ivy.to_numpy(ivy.array([6, 7, 8])))
        assert np.allclose(ivy.to_numpy(self._dataset[3].x), ivy.to_numpy(ivy.array([9, 0, 1])))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single_wrapped(self, dev_str, f, call, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[3].x), ivy.to_numpy(ivy.array([9, 0, 1])))
        assert np.allclose(ivy.to_numpy(self._dataset[4].x), ivy.to_numpy(ivy.array([2, 3, 4])))
        assert np.allclose(ivy.to_numpy(self._dataset[5].x), ivy.to_numpy(ivy.array([5, 6, 7])))
        assert np.allclose(ivy.to_numpy(self._dataset[6].x), ivy.to_numpy(ivy.array([8, 9, 0])))
        assert np.allclose(ivy.to_numpy(self._dataset[7].x), ivy.to_numpy(ivy.array([1, 2, 3])))
        assert np.allclose(ivy.to_numpy(self._dataset[8].x), ivy.to_numpy(ivy.array([4, 5, 6])))
        assert np.allclose(ivy.to_numpy(self._dataset[9].x), ivy.to_numpy(ivy.array([7, 8, 9])))

        assert np.allclose(ivy.to_numpy(self._dataset[-1].x), ivy.to_numpy(ivy.array([7, 8, 9])))
        assert np.allclose(ivy.to_numpy(self._dataset[-2].x), ivy.to_numpy(ivy.array([4, 5, 6])))
        assert np.allclose(ivy.to_numpy(self._dataset[-3].x), ivy.to_numpy(ivy.array([1, 2, 3])))
        assert np.allclose(ivy.to_numpy(self._dataset[-4].x), ivy.to_numpy(ivy.array([8, 9, 0])))
        assert np.allclose(ivy.to_numpy(self._dataset[-5].x), ivy.to_numpy(ivy.array([5, 6, 7])))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice(self, dev_str, f, call, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[0]), ivy.to_numpy(ivy.array([0, 1, 2])))
        assert np.allclose(ivy.to_numpy(self._dataset[0:2].x[1]), ivy.to_numpy(ivy.array([3, 4, 5])))
        assert np.allclose(ivy.to_numpy(self._dataset[2:3].x[0]), ivy.to_numpy(ivy.array([6, 7, 8])))

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice_wrapped(self, dev_str, f, call, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        self._init(num_processes)

        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[0]), ivy.to_numpy(ivy.array([7, 8, 9])))
        assert np.allclose(ivy.to_numpy(self._dataset[-1:1].x[1]), ivy.to_numpy(ivy.array([0, 1, 2])))
        assert np.allclose(ivy.to_numpy(self._dataset[2:4].x[0]), ivy.to_numpy(ivy.array([6, 7, 8])))
        assert np.allclose(ivy.to_numpy(self._dataset[2:4].x[1]), ivy.to_numpy(ivy.array([9, 0, 1])))

        # close
        self._dataset.close()
        del self._dataset


class TestShuffle:

    def _init(self, array_shape, num_processes):
        x = [ivy.array(0), ivy.array(1), ivy.array(2),
             ivy.array(3), ivy.array(4), ivy.array(5),
             ivy.array(6), ivy.array(7), ivy.array(8)]
        self._x = [ivy.reshape(item, array_shape) for item in x]
        dataset_container = ivy.Container({'x': self._x})
        self._dataset = MapDataset(
            dataset_container, 'base', dataset_container.shape[0], num_processes=num_processes).shuffle('shuffled', 9)

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        ivy.seed(0)
        np.random.seed(0)
        self._init(array_shape, num_processes)

        assert list(self._dataset[0].x.shape) == array_shape
        assert list(self._dataset[4].x.shape) == array_shape
        assert list(self._dataset[8].x.shape) == array_shape

        check0 = not np.allclose(ivy.to_numpy(self._dataset[0].x), ivy.to_numpy(self._x[0]))
        check1 = not np.allclose(ivy.to_numpy(self._dataset[1].x), ivy.to_numpy(self._x[1]))
        check2 = not np.allclose(ivy.to_numpy(self._dataset[2].x), ivy.to_numpy(self._x[2]))
        check3 = not np.allclose(ivy.to_numpy(self._dataset[3].x), ivy.to_numpy(self._x[3]))
        check4 = not np.allclose(ivy.to_numpy(self._dataset[4].x), ivy.to_numpy(self._x[4]))
        check5 = not np.allclose(ivy.to_numpy(self._dataset[5].x), ivy.to_numpy(self._x[5]))
        check6 = not np.allclose(ivy.to_numpy(self._dataset[6].x), ivy.to_numpy(self._x[6]))
        check7 = not np.allclose(ivy.to_numpy(self._dataset[7].x), ivy.to_numpy(self._x[7]))
        check8 = not np.allclose(ivy.to_numpy(self._dataset[8].x), ivy.to_numpy(self._x[8]))

        assert check0 or check1 or check2 or check3 or check4 or check5 or check6 or check7 or check8

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_single_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        ivy.seed(0)
        np.random.seed(0)
        self._init(array_shape, num_processes)

        assert list(self._dataset[9].x.shape) == array_shape
        assert list(self._dataset[11].x.shape) == array_shape
        assert list(self._dataset[-1].x.shape) == array_shape
        assert list(self._dataset[-2].x.shape) == array_shape

        check0 = not np.allclose(ivy.to_numpy(self._dataset[9].x), ivy.to_numpy(self._x[0]))
        check1 = not np.allclose(ivy.to_numpy(self._dataset[11].x), ivy.to_numpy(self._x[2]))
        check2 = not np.allclose(ivy.to_numpy(self._dataset[-1].x), ivy.to_numpy(self._x[-1]))
        check3 = not np.allclose(ivy.to_numpy(self._dataset[-2].x), ivy.to_numpy(self._x[-2]))

        assert check0 or check1 or check2 or check3

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        ivy.seed(0)
        np.random.seed(0)
        self._init(array_shape, num_processes)

        assert len(self._dataset[0:3].x) == 3
        assert list(self._dataset[0:3].x[0].shape) == array_shape
        assert len(self._dataset[3:6].x) == 3
        assert list(self._dataset[3:6].x[0].shape) == array_shape
        assert len(self._dataset[6:9].x) == 3
        assert list(self._dataset[6:9].x[0].shape) == array_shape

        check0 = not np.allclose(ivy.to_numpy(self._dataset[0:3].x[0]), ivy.to_numpy(self._x[0]))
        check1 = not np.allclose(ivy.to_numpy(self._dataset[3:6].x[1]), ivy.to_numpy(self._x[4]))
        check2 = not np.allclose(ivy.to_numpy(self._dataset[6:9].x[0]), ivy.to_numpy(self._x[6]))
        check3 = not np.allclose(ivy.to_numpy(self._dataset[6:9].x[1]), ivy.to_numpy(self._x[7]))

        assert check0 or check1 or check2 or check3

        # close
        self._dataset.close()
        del self._dataset

    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "num_processes", [1, 2])
    def test_slice_wrapped(self, dev_str, f, call, array_shape, num_processes):

        if call in [helpers.jnp_call, helpers.mx_call] and num_processes == 2:
            pytest.skip()

        ivy.seed(0)
        np.random.seed(0)
        self._init(array_shape, num_processes)

        assert len(self._dataset[-1:1].x) == 2
        assert list(self._dataset[-1:1].x[0].shape) == array_shape
        assert len(self._dataset[-1:1].x) == 2
        assert list(self._dataset[-1:1].x[1].shape) == array_shape
        assert len(self._dataset[9:11].x) == 2
        assert list(self._dataset[9:11].x[0].shape) == array_shape
        assert len(self._dataset[9:11].x) == 2
        assert list(self._dataset[9:11].x[0].shape) == array_shape

        check0 = not np.allclose(ivy.to_numpy(self._dataset[-1:1].x[0]), ivy.to_numpy(self._x[8]))
        check1 = not np.allclose(ivy.to_numpy(self._dataset[-1:1].x[1]), ivy.to_numpy(self._x[0]))
        check2 = not np.allclose(ivy.to_numpy(self._dataset[9:11].x[0]), ivy.to_numpy(self._x[0]))
        check3 = not np.allclose(ivy.to_numpy(self._dataset[9:11].x[1]), ivy.to_numpy(self._x[1]))

        assert check0 or check1 or check2 or check3

        # close
        self._dataset.close()
        del self._dataset


class TestPrefetch:

    def _init(self, array_shape, parallel_method):
        x = [ivy.array(0), ivy.array(1), ivy.array(2), ivy.array(3), ivy.array(4),
             ivy.array(5), ivy.array(6), ivy.array(7), ivy.array(8), ivy.array(9)]
        self._x = [ivy.reshape(item, array_shape) for item in x]
        dataset_container = ivy.Container({'x': self._x})
        dataset = MapDataset(dataset_container, 'base', dataset_container.shape[0], with_caching=False, cache_size=0)

        def sleep_fn(cont):
            time.sleep(0.05)
            return cont

        self._dataset_wo_prefetch = dataset.map('sleep', sleep_fn)
        self._dataset_w_prefetch = self._dataset_wo_prefetch.to_iterator('prefetch', parallel_method=parallel_method)

    # noinspection PyStatementEffect
    @pytest.mark.parametrize(
        "array_shape", [[1], []])
    @pytest.mark.parametrize(
        "parallel_method", ["thread", "process"])
    def test_single(self, dev_str, f, call, array_shape, parallel_method):

        if call is helpers.mx_call:
            # For some reason, mxnet causes this to hang. Further, array_shape == [] and parallel_method == 'process'
            # causes ret = self._output_queue.get(timeout=self._prefetch_timeout) in method _get_from_process in
            # IteratorDataset class to hang, and then timeout with queue.Emppty exception.
            pytest.skip()

        self._init(array_shape, parallel_method)

        for i in range(10):
            start_time = time.perf_counter()
            self._dataset_wo_prefetch[i]
            assert time.perf_counter() - start_time > 0.05

        for i in range(10):
            start_time = time.perf_counter()
            next(self._dataset_w_prefetch)
            if i > 0:
                assert time.perf_counter() - start_time < 0.05
            time.sleep(0.05)

        # delete
        self._dataset_wo_prefetch.__del__()
        del self._dataset_wo_prefetch
        self._dataset_w_prefetch.__del__()
        del self._dataset_w_prefetch
