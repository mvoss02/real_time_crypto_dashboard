from datetime import datetime, timedelta

import hopsworks
import pandas as pd
from hsfs.feature_group import FeatureGroup
from hsfs.feature_store import FeatureStore
from hsfs.feature_view import FeatureView
from loguru import logger


class FeatureReader:
    """
    Reads features from our 2 features groups
    - technical_indicators
    - news_signals
    and preprocess it so that it has the format (features, target) we need for
    training and for inference.
    """

    def __init__(
        self,
        hopsworks_project_name: str,
        hopsworks_api_key: str,
        feature_group_name: str,
        feature_group_version: int,
        feature_view_name: str,
        feature_view_version: int,
    ):
        self.feature_group_name = feature_group_name
        self.feature_view_name = feature_view_name

        # Connect to the feature store
        self._feature_store = self._get_feature_store(
            hopsworks_project_name,
            hopsworks_api_key,
        )

        # Get feature group (NOTE: we can do that here because we only have one feature grouzp at the moment)
        self._feature_group = self._get_feature_group(
            name=feature_group_name, version=feature_group_version
        )

        # Get feature view (if it exists, othwerwise create)
        self._feature_view = self._get_feature_view(
            feature_view_name,
            feature_view_version,
        )

    def _get_feature_group(self, name: str, version: int) -> FeatureGroup:
        """
        Returns a feature group object given its name and version
        """
        return self._feature_store.get_feature_group(
            name=name,
            version=version,
        )

    def _get_feature_view(
        self, feature_view_name: str, feature_view_version: int
    ) -> FeatureView:
        """
        Returns a feature view object given its name and version.
        """
        try:
            # If no query is provided, select all columns from the feature group
            query = self._feature_group.select_all()

            return self._feature_store.get_or_create_feature_view(
                name=feature_view_name, version=feature_view_version, query=query
            )
        except Exception as e:
            logger.error(f'Could not create or fetch the feature view. Error: {e}')
            raise

    def _get_feature_store(self, project_name: str, api_key: str) -> FeatureStore:
        """
        Returns a feature store object.
        """
        logger.info('Getting feature store')
        project = hopsworks.login(project=project_name, api_key_value=api_key)
        fs = project.get_feature_store()
        return fs

    def get_data(self, n_days: int) -> pd.DataFrame:
        """
        Use the self._feature_view to get the an initial dataset going back `n_days` days.
        """
        # Data from feature store
        logger.info(f'Getting data going back {n_days} days')
        data = self._feature_view.get_batch_data(
            start_time=datetime.now() - timedelta(days=n_days),
            end_time=datetime.now(),
            dataframe_type='pandas',
        )

        return data


if __name__ == '__main__':
    import time

    from config.config import hopsworksCredentialsConfig, hopsworksSettingsConfig

    reader = FeatureReader(
        hopsworks_project_name=hopsworksCredentialsConfig.project_name,
        hopsworks_api_key=hopsworksCredentialsConfig.api_key,
        feature_group_name=hopsworksSettingsConfig.feature_group_name,
        feature_group_version=hopsworksSettingsConfig.feature_group_version,
        feature_view_name=hopsworksSettingsConfig.feature_view_name,
        feature_view_version=hopsworksSettingsConfig.feature_view_version,
    )

    try:
        df = reader.get_data(n_days=10)
        logger.info(f'Fetched data successfully: {df}')
    except Exception as e:
        logger.error(f'Failed to fetch data from feature view. Error: {e}')
        raise

    try:
        waiting_sec = 20
        logger.info(f'Sleeping for {waiting_sec}')
        time.sleep(waiting_sec)
        df_new_data = reader.get_data(n_days=1)
        logger.info(f'Fetched data successfully: {df_new_data}')
    except Exception as e:
        logger.error(f'Failed to fetch data from feature view. Error: {e}')
        raise
