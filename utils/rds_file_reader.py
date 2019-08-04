import pyreadr


## Open RDS File Convert to HTML
def rds_to_html(file_path):

    app_rds = pyreadr.read_r(file_path)
    app_df = app_rds[None]
    app_html = app_df.iloc[0, 0]

    return app_html



