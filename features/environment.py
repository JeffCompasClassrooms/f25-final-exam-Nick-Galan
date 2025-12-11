import os
import tempfile


def before_all(context):
    context.behave_driver = None
    try:
        import behave_webdriver

        try:
            
            context.behave_driver = behave_webdriver.Chrome.headless()
        except Exception as e:
        
            print("WARN: could not start Chrome headless via behave_webdriver:", e)
            context.behave_driver = None
    except ImportError:
      
        print("WARN: behave_webdriver is not installed; skipping browser setup")
        context.behave_driver = None


def after_all(context):
    driver = getattr(context, "behave_driver", None)
    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass


def before_scenario(context, scenario):
    context.tempdir = tempfile.TemporaryDirectory()
    context.christmas_list_file = os.path.join(context.tempdir.name, "christmas_list.pkl")


def after_scenario(context, scenario):
    context.tempdir.cleanup()
